import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, sep } from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { assetName, childEnvironment, downloadVerified, hermesModelSelection, installPlan, parseWindowsLauncher,
  redact, safeRelativePath, selectSkillEntries, validateAmount, validateModel, validateProxy,
  validateToken, verifyGitBlob, workbuddyProvider, writePreserving } from '../lib/core.mjs';

test('supported platform mapping rejects unsupported binaries', () => {
  assert.equal(assetName('win32', 'x64'), 'magpie-cli-windows-amd64.exe');
  assert.equal(assetName('darwin', 'arm64'), 'magpie-cli-darwin-arm64');
  assert.throws(() => assetName('linux', 'ia32'));
});
test('path traversal and absolute paths never reach the skill writer', () => {
  for (const value of ['../session.json', '/etc/passwd', 'C:/file', 'a\\b', 'a/../b', 'a//b']) {
    assert.throws(() => safeRelativePath(value));
  }
  assert.equal(safeRelativePath('references/authentication.md'), 'references/authentication.md');
});
test('skill tree requires complete entries and disallows symlinks', () => {
  const path = 'skills/binance-web3/binance-agentic-wallet/SKILL.md';
  const entry = { path, type: 'blob', mode: '100644', size: 10, sha: 'abc' };
  assert.equal(selectSkillEntries({ tree: [entry] }, ['binance-agentic-wallet']).length, 1);
  assert.throws(() => selectSkillEntries({ truncated: true, tree: [entry] }, ['binance-agentic-wallet']));
  assert.throws(() => selectSkillEntries({ tree: [{ ...entry, mode: '120000' }] }, ['binance-agentic-wallet']));
  assert.throws(() => selectSkillEntries({ tree: [] }, ['binance-agentic-wallet']));
});
test('download integrity failure stops before creating executable', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'wallet-starter-test-'));
  try {
    const target = join(dir, 'magpie');
    await assert.rejects(downloadVerified('https://example.test/', 'a'.repeat(64), target,
      async () => Buffer.from('modified executable')), /SHA-256/);
    assert.equal(existsSync(target), false);
  } finally {
    assert.ok(resolve(dir).startsWith(resolve(tmpdir()) + sep + 'wallet-starter-test-'));
    await rm(dir, { recursive: true });
  }
});
test('modified local skills are preserved instead of overwritten', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'wallet-starter-test-'));
  try {
    const file = join(dir, 'SKILL.md');
    await writePreserving(file, Buffer.from('my existing skill'));
    assert.equal(await writePreserving(file, Buffer.from('my existing skill')), false);
    await assert.rejects(writePreserving(file, Buffer.from('replacement')));
    assert.equal(await readFile(file, 'utf8'), 'my existing skill');
  } finally {
    assert.ok(resolve(dir).startsWith(resolve(tmpdir()) + sep + 'wallet-starter-test-'));
    await rm(dir, { recursive: true });
  }
});
test('Git blob validation uses the Git header and rejects modified content', () => {
  const bytes = Buffer.from('official skill\n');
  const sha = createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
  assert.doesNotThrow(() => verifyGitBlob(bytes, sha));
  assert.throws(() => verifyGitBlob(Buffer.from('different'), sha));
});
test('quote preserves exact decimal amount and full contract', () => {
  assert.equal(validateAmount('0.0001'), '0.0001');
  for (const x of ['0', '-1', '1e-4', 'NaN', '1;echo x', '0.0000000000000000001']) assert.throws(() => validateAmount(x));
  assert.equal(validateToken('0x55d398326f99059fF775485246999027B3197955').length, 42);
  assert.throws(() => validateToken('USDT'));
});
test('only the selected WorkBuddy region/model is accepted', () => {
  assert.equal(workbuddyProvider(), 'workbuddy-ai');
  assert.equal(workbuddyProvider('cn'), 'workbuddy');
  assert.throws(() => workbuddyProvider('unknown'));
  assert.equal(validateModel('workbuddy-ai/actual-model-id'), 'workbuddy-ai/actual-model-id');
  assert.throws(() => validateModel('openrouter/paid-model'));
  assert.throws(() => validateModel('workbuddy-ai/model; command'));
});
test('Hermes model selection includes Magpie provider prefix', () => {
  assert.deepEqual(hermesModelSelection('workbuddy-ai/model-id'), ['hermes', 'magpie/workbuddy-ai/model-id']);
  assert.throws(() => hermesModelSelection('unknown/model'));
});
test('child proxy settings do not change the parent or proxy localhost', () => {
  const parent = { PATH: '/usr/bin', HOME: '/original-home' };
  const env = childEnvironment('/starter', 'http://127.0.0.1:7890', parent);
  assert.equal(parent.HTTPS_PROXY, undefined);
  assert.equal(env.HOME, parent.HOME);
  assert.match(env.NO_PROXY, /127\.0\.0\.1/);
  assert.equal(env.NODE_USE_ENV_PROXY, '1');
  assert.throws(() => validateProxy('http://user:secret@127.0.0.1:7890'));
  assert.throws(() => validateProxy('file:///tmp/proxy'));
});
test('credentials are masked in structured errors', () => {
  const text = redact('{"clientId":"private-client", "accessToken":"private-access", "message":"bad"}');
  assert.ok(!text.includes('private-client'));
  assert.ok(!text.includes('private-access'));
  assert.ok(text.includes('bad'));
});
test('Windows Hermes launcher uses argv without executing cmd.exe', () => {
  const launch = parseWindowsLauncher('@echo off\r\n"C:\\Hermes Path\\python.exe" -I -c "exec(\'safe-generated-code\')" %*\r\n');
  assert.equal(launch.file, 'C:\\Hermes Path\\python.exe');
  assert.deepEqual(launch.prefix, ['-I', '-c', "exec('safe-generated-code')"]);
  assert.throws(() => parseWindowsLauncher('cmd /c arbitrary'));
});
test('install plan never authenticates or trades', async () => {
  const versions = JSON.parse(await readFile(new URL('../versions.json', import.meta.url), 'utf8'));
  const plan = installPlan(versions, 'win32', 'x64');
  assert.equal(plan.automaticLogin, false);
  assert.equal(plan.automaticTrade, false);
  assert.ok(!('opencode-ai' in plan.npm));
  assert.throws(() => installPlan(versions, 'darwin', 'x64'), /Intel Mac/);
  assert.equal(installPlan(versions, 'darwin', 'x64', true).hermes, 'skip');
  const result = spawnSync(process.execPath, [fileURLToPath(new URL('../starter.mjs', import.meta.url)), 'install', '--dry-run'],
    { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /"automaticTrade": false/);
});
