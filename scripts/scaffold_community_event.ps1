param(
  [Parameter(Mandatory = $true)]
  [string]$Title,
  [Parameter(Mandatory = $true)]
  [string]$Date,
  [Parameter(Mandatory = $true)]
  [string]$Mode,
  [Parameter(Mandatory = $true)]
  [string]$Summary,
  [Parameter(Mandatory = $true)]
  [string]$CtaLabel,
  [Parameter(Mandatory = $true)]
  [string]$CtaHref,
  [string]$FilePath = 'db/community_events.json'
)

$ErrorActionPreference = 'Stop'

function Normalize-Arg {
  param([string]$Value)
  if ($null -eq $Value) { return '' }
  $trimmed = $Value.Trim()
  if ($trimmed -eq '.') { return '' }
  return $trimmed
}

$Title = Normalize-Arg $Title
$Date = Normalize-Arg $Date
$Mode = Normalize-Arg $Mode
$Summary = Normalize-Arg $Summary
$CtaLabel = Normalize-Arg $CtaLabel
$CtaHref = Normalize-Arg $CtaHref
$FilePath = Normalize-Arg $FilePath

if ([string]::IsNullOrWhiteSpace($FilePath)) {
  throw 'FilePath is required.'
}
if (-not (Test-Path $FilePath)) {
  throw ('Target file not found: ' + $FilePath)
}

foreach ($pair in @(
  @{Name='Title';Value=$Title},
  @{Name='Date';Value=$Date},
  @{Name='Mode';Value=$Mode},
  @{Name='Summary';Value=$Summary},
  @{Name='CtaLabel';Value=$CtaLabel},
  @{Name='CtaHref';Value=$CtaHref}
)) {
  if ([string]::IsNullOrWhiteSpace($pair.Value)) {
    throw ($pair.Name + ' is required and cannot be empty or "."')
  }
}

if ($Date -notmatch '^\d{4}-\d{2}-\d{2}$') {
  throw 'Date must use YYYY-MM-DD format.'
}

if ($CtaHref -notmatch '^(https?://|[^:?#]+(\?[^#]*)?(#.*)?$)') {
  throw 'CtaHref must be an http(s) URL or a local path.'
}

$raw = Get-Content -Raw $FilePath
try {
  $doc = $raw | ConvertFrom-Json
} catch {
  throw ('Invalid JSON in target file: ' + $FilePath)
}

if ($null -eq $doc.events -or $doc.events -isnot [System.Array]) {
  throw 'Target JSON must contain an events array.'
}

$event = [ordered]@{
  title = $Title
  date = $Date
  mode = $Mode
  summary = $Summary
  ctaLabel = $CtaLabel
  ctaHref = $CtaHref
}

$doc.events += [pscustomobject]$event

$json = $doc | ConvertTo-Json -Depth 8
Set-Content -Path $FilePath -Value ($json + [Environment]::NewLine)

Write-Host ('Appended event to ' + $FilePath)
Write-Host ('Total events: ' + $doc.events.Count)
