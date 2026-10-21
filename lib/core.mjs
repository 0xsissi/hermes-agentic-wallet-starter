import { createHash } from 'node:crypto';
import { spawn, spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdir, readFile, writeFile, chmod } from 'node:fs/promises';
import { dirname, join, resolve, delimiter } from 'node:path';

export function assetName(platform = process.platform, arch = process.arch) {
  const os = { win32: 'windows', darwin: 'darwin', linux: 'linux' }[platform];
  const cpu = { x64: 'amd64', arm64: 'arm64' }[arch];
  if (!os || !cpu) throw new Error('只支持 Windows/macOS/Linux 的 x64 和 arm64。');
  return `magpie-cli-${os}-${cpu}${platform === 'win32' ? '.exe' : ''}`;
}

export function verifySha256(bytes, expected) {
  if (!/^[a-f0-9]{64}$/i.test(expected)) throw new Error('缺少可信 SHA-256。');
  if (createHash('sha256').update(bytes).digest('hex') !== expected.toLowerCase()) {
    throw new Error('SHA-256 不匹配，已停止。请勿跳过校验。');
  }
}

export function verifyGitBlob(bytes, expected) {
  const digest = createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
  if (digest !== expected) throw new Error('Git 文件哈希不匹配。');
}

export function safeRelativePath(path) {
  if (!path || path.includes('\\') || path.includes(':') || path.startsWith('/') ||
      path.split('/').some(p => !p || p === '.' || p === '..')) {
    throw new Error('不安全的相对路径。');
  }
  return path;
}

export function validateToken(address) {
  if (!/^0x[0-9a-fA-F]{40}$/.test(address ?? '')) throw new Error('请输入 BSC 代币完整合约地址。');
  return address;
}

export function validateAmount(amount) {
  if (!/^(?:0|[1-9]\d*)(?:\.\d{1,18})?$/.test(amount ?? '') ||
      !/[1-9]/.test(amount)) throw new Error('金额须为正数，最多 18 位小数，不接受科学计数法。');
  return amount;
}

export function workbuddyProvider(region = 'intl') {
  if (region === 'intl') return 'workbuddy-ai';
  if (region === 'cn') return 'workbuddy';
  throw new Error('region 只能是 intl 或 cn。');
}

export function validateModel(model) {
  if (!/^(workbuddy-ai|workbuddy)\/[A-Za-z0-9][A-Za-z0-9._:/-]*$/.test(model ?? '')) {
    throw new Error('只接受模型列表中的 workbuddy-ai/… 或 workbuddy/… 完整 ID。');
  }
  return model;
}

export function hermesModelSelection(model) {
  return ['hermes', `magpie/${validateModel(model)}`];
}

export function redact(value) {
  return String(value).replace(/((?:agentSessionId|sessionId|sessionToken|clientId|accessToken|refreshToken|apiKey|api_key|privateKey|password)["']?\s*[:=]\s*["']?)[^\s"',;}]+/gi, '$1[REDACTED]');
}

export function parseWindowsLauncher(text) {
  const match = text.match(/^\s*"([^"\r\n]+python(?:\.exe)?)"\s+-I\s+-c\s+"([^"\r\n]+)"\s+%\*\s*$/mi);
  if (!match) throw new Error('无法识别官方 Hermes .cmd 启动器。');
  return { file: match[1], prefix: ['-I', '-c', match[2]] };
}

export async function writePreserving(path, bytes) {
  if (existsSync(path)) {
    const current = await readFile(path);
    if (Buffer.compare(current, Buffer.from(bytes)) !== 0) {
      throw new Error(`文件已存在且内容不同，已保留：${path}`);
    }
    return false;
  }
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, bytes, { flag: 'wx', mode: 0o600 });
  return true;
}

export function findNpmCli(env = process.env) {
  const dirs = [dirname(process.execPath), ...(env.PATH || env.Path || '').split(delimiter)];
  for (const dir of dirs) {
    for (const candidate of [join(dir, 'node_modules/npm/bin/npm-cli.js'),
      resolve(dir, '../lib/node_modules/npm/bin/npm-cli.js'),
      resolve(dir, '../share/nodejs/npm/bin/npm-cli.js')]) {
      if (existsSync(candidate)) return candidate;
    }
  }
  throw new Error('未找到 npm。请从 nodejs.org 安装 Node.js 24 LTS（包含 npm），重开终端。');
}

export function powershellExecutable(env = process.env) {
  const paths = (env.PATH || env.Path || '').split(delimiter);
  const candidates = [...paths.map(p => join(p, 'pwsh.exe')),
    join(env.ProgramFiles || 'C:\\Program Files', 'PowerShell', '7', 'pwsh.exe')];
  return candidates.find(existsSync) || 'powershell.exe';
}

export function run(file, args = [], { env = process.env, cwd, inherit = false, timeout = 0 } = {}) {
  return new Promise((ok, fail) => {
    const child = spawn(file, args, { env, cwd, shell: false, windowsHide: true,
      stdio: inherit ? 'inherit' : ['ignore', 'pipe', 'pipe'] });
    let output = '';
    const collect = data => {
      output += data.toString();
      if (output.length > 4 * 1024 * 1024) child.kill();
    };
    child.stdout?.on('data', collect);
    child.stderr?.on('data', collect);
    const timer = timeout ? setTimeout(() => child.kill(), timeout) : undefined;
    child.on('error', error => { clearTimeout(timer); fail(error); });
    child.on('close', code => {
      clearTimeout(timer);
      if (code !== 0) fail(new Error(redact(output.trim()) || `${file} 退出，状态 ${code}`));
      else ok(output.trim());
    });
  });
}

export function validateProxy(proxy) {
  const url = new URL(proxy);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
    throw new Error('只接受不含用户名密码的 HTTP(S) 代理 URL。');
  }
  return url.href;
}

export function childEnvironment(root, proxy, base = process.env) {
  const env = { ...base };
  env.HERMES_HOME = join(root, '.runtime', 'hermes-home');
  env.BINANCE_BAW_DIR = join(root, '.runtime', 'baw');
  env.UV_CACHE_DIR = join(root, '.runtime', 'uv-cache');
  env.UV_PYTHON_INSTALL_DIR = join(root, '.runtime', 'bootstrap-python');
  env.PATH = [join(root, '.runtime', 'npm', 'node_modules', '.bin'),
    join(root, '.runtime', 'bin'), join(env.HERMES_HOME, 'bin'), env.PATH || env.Path || ''].join(delimiter);
  env.NO_PROXY = [env.NO_PROXY || env.no_proxy || '', '127.0.0.1', 'localhost', '[::1]'].filter(Boolean).join(',');
  if (proxy) {
    env.HTTP_PROXY = validateProxy(proxy);
    env.HTTPS_PROXY = validateProxy(proxy);
    env.NODE_USE_ENV_PROXY = '1';
  }
  return env;
}

export function windowsSystemProxy() {
  if (process.platform !== 'win32') return '';
  const script = "$p=Get-ItemProperty -LiteralPath 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'; if($p.ProxyEnable -eq 1){$p.ProxyServer}";
  const r = spawnSync(powershellExecutable(), ['-NoProfile', '-NonInteractive', '-Command', script],
    { encoding: 'utf8', windowsHide: true, timeout: 5000 });
  const raw = (r.stdout || '').trim();
  const match = raw.match(/(?:^|(?:https|http)=)((?:127\.0\.0\.1|localhost):\d+)(?:;|$)/);
  return match ? `http://${match[1]}` : '';
}

export async function download(url, limit = 80 * 1024 * 1024) {
  const u = new URL(url);
  if (u.protocol !== 'https:') throw new Error('下载只接受 HTTPS。');
  const response = await fetch(u, { headers: { 'User-Agent': 'hermes-agentic-wallet-starter/0.1' },
    signal: AbortSignal.timeout(120000) });
  if (!response.ok) throw new Error(`下载失败 HTTP ${response.status}：${u.hostname}。请检查网络或 GitHub 限流。`);
  let size = 0;
  const parts = [];
  for await (const part of response.body) {
    size += part.length;
    if (size > limit) throw new Error('下载超出体积上限。');
    parts.push(part);
  }
  return Buffer.concat(parts);
}

export async function downloadVerified(url, sha, path, fetcher = download) {
  if (existsSync(path)) { verifySha256(await readFile(path), sha); return; }
  const bytes = await fetcher(url);
  verifySha256(bytes, sha);
  await writePreserving(path, bytes);
  if (process.platform !== 'win32') await chmod(path, 0o700);
}

export function selectSkillEntries(tree, names) {
  if (tree.truncated || !Array.isArray(tree.tree)) throw new Error('上游文件列表不完整。');
  const entries = [];
  for (const name of names) {
    const prefix = `skills/binance-web3/${name}/`;
    const files = tree.tree.filter(f => f.path.startsWith(prefix) && f.type === 'blob');
    if (!files.some(f => f.path === `${prefix}SKILL.md`)) throw new Error(`缺少官方技能 ${name}`);
    for (const f of files) {
      if (!['100644', '100755'].includes(f.mode)) throw new Error('拒绝技能中的符号链接。');
      const relative = safeRelativePath(f.path.slice(prefix.length));
      if (f.size > 2 * 1024 * 1024) throw new Error('技能文件过大。');
      entries.push({ ...f, name, relative });
    }
  }
  if (entries.length > 200) throw new Error('技能文件数量异常。');
  return entries;
}

export function installPlan(versions, platform = process.platform, arch = process.arch, skipHermes = false) {
  if (platform === 'darwin' && arch === 'x64' && !skipHermes) {
    throw new Error('Hermes 当前官方不支持 Intel Mac。请使用受支持设备；--skip-hermes 仅安装其余组件。');
  }
  const asset = assetName(platform, arch);
  if (!versions.magpie.assets[asset]) throw new Error('没有该平台的校验信息。');
  return { platform, arch, magpie: { version: versions.magpie.version, asset },
    npm: versions.npm, skillCommit: versions.skills.commit, skills: versions.skills.names,
    hermes: skipHermes ? 'skip' : 'official-stable-installer',
    automaticLogin: false, automaticTrade: false,
    notes: ['安装到本项目 .runtime；Hermes 官方安装器可能添加用户级启动路径。',
      '安装不会自动登录 WorkBuddy 或币安，不会自动发起交易。',
      '插件将在 workbuddy-login 时添加到用户的 Magpie 配置。'] };
}
