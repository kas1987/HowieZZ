param(
  [Parameter(Position = 0)]
  [object]$SourcePath = '_local/reference/zelexdoll-theme/docs/community_channels.json'
)

# Harden argument handling: ignore placeholder '.' input for accidental invocation.
$resolvedSource = [string]$SourcePath
if (-not $resolvedSource -or $resolvedSource -eq '.') {
  $resolvedSource = '_local/reference/zelexdoll-theme/docs/community_channels.json'
}

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$dest = Join-Path $root 'db/community_channels.json'
$src = if ([System.IO.Path]::IsPathRooted($resolvedSource)) { $resolvedSource } else { Join-Path $root $resolvedSource }

if (-not (Test-Path $src)) {
  Write-Host ('No source file found at: ' + $src)
  Write-Host 'No changes made. Provide a source path argument when available.'
  exit 0
}

try {
  $raw = Get-Content -Path $src -Raw -Encoding UTF8
  $null = $raw | ConvertFrom-Json
} catch {
  Write-Error ('Source is not valid JSON: ' + $src)
  exit 1
}

$raw | Set-Content -Path $dest -Encoding UTF8
Write-Host ('Synced community channels from: ' + $src)
Write-Host ('Destination updated: ' + $dest)
