param(
  [Parameter(Position = 0)]
  [object]$Iterations = 1
)

# Harden argument handling: ignore placeholder args like '.' and non-numeric values.
$loopCount = 1
if ($null -ne $Iterations) {
  $raw = [string]$Iterations
  if ($raw -and $raw -ne '.') {
    $tmp = 1
    if ([int]::TryParse($raw, [ref]$tmp) -and $tmp -gt 0) {
      $loopCount = $tmp
    }
  }
}

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$dest = Join-Path $root 'v2 HTML'
if (-not (Test-Path $dest)) {
  New-Item -Path $dest -ItemType Directory | Out-Null
}

$sourceFiles = Get-ChildItem -Path $root -File -Filter '*.html' |
  Where-Object { $_.DirectoryName -eq $root } |
  Sort-Object Name

if (-not $sourceFiles -or $sourceFiles.Count -eq 0) {
  throw 'No root HTML files found for v2 packaging.'
}

for ($i = 1; $i -le $loopCount; $i++) {
  foreach ($file in $sourceFiles) {
    Copy-Item -Path $file.FullName -Destination (Join-Path $dest $file.Name) -Force
  }
}

$manifestEntries = @()
$shaLines = @()
$destFiles = Get-ChildItem -Path $dest -File -Filter '*.html' | Sort-Object Name

foreach ($file in $destFiles) {
  $hash = Get-FileHash -Path $file.FullName -Algorithm SHA256
  $manifestEntries += [PSCustomObject]@{
    file = $file.Name
    size_bytes = $file.Length
    sha256 = $hash.Hash.ToLowerInvariant()
    modified_utc = $file.LastWriteTimeUtc.ToString('o')
  }
  $shaLines += ($hash.Hash.ToLowerInvariant() + '  ' + $file.Name)
}

$manifest = [PSCustomObject]@{
  generated_utc = (Get-Date).ToUniversalTime().ToString('o')
  source_root = $root
  destination = $dest
  file_count = $manifestEntries.Count
  loop_count = $loopCount
  files = $manifestEntries
}

$manifestPath = Join-Path $dest 'manifest.json'
$shaPath = Join-Path $dest 'manifest.sha256'

$manifest | ConvertTo-Json -Depth 5 | Set-Content -Path $manifestPath -Encoding UTF8
$shaLines | Set-Content -Path $shaPath -Encoding UTF8

Write-Host ('Packaged ' + $manifestEntries.Count + ' HTML files to v2 HTML. loop_count=' + $loopCount)
Write-Host ('Manifest: ' + $manifestPath)
Write-Host ('Checksums: ' + $shaPath)
