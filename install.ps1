[CmdletBinding()]
param([switch]$DryRun, [switch]$SkipHermes, [string]$Proxy = '')
$ErrorActionPreference = 'Stop'
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host 'Install Node.js 24 LTS from https://nodejs.org/ first, then reopen PowerShell.'
    exit 1
}
$starterArgs = @((Join-Path $PSScriptRoot 'starter.mjs'), 'install')
if ($DryRun) { $starterArgs += '--dry-run' }
if ($SkipHermes) { $starterArgs += '--skip-hermes' }
if ($Proxy) { $starterArgs += @('--proxy', $Proxy) }
& node @starterArgs
exit $LASTEXITCODE
