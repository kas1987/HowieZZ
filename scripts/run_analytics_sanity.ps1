<#
Config schema expected at docs/pdr/PDR-analytics-sanity-thresholds.json:
{
  "schemaVersion": "2026-06-06",
  "source": "howiezz-web",
  "positiveFixture": {
    "input": "docs/pdr/PDR-analytics-sample-events.ndjson",
    "minTotalEvents": 8,
    "minPageViews": 2,
    "minCompareAdd": 1,
    "minInquiryAttempts": 1,
    "minAttributionCoverage": 0.8
  }
}
#>

Param(
  [string]$InputPath = "docs/pdr/PDR-analytics-sample-events.ndjson",
  [string]$SchemaVersion = "2026-06-06",
  [string]$Source = "howiezz-web",
  [string]$ConfigPath = "docs/pdr/PDR-analytics-sanity-thresholds.json",
  [string]$OutputJson = "",
  [int]$MinTotalEvents = 8,
  [int]$MinPageViews = 2,
  [int]$MinCompareAdd = 1,
  [int]$MinInquiryAttempts = 1,
  [double]$MinAttributionCoverage = 0.8,
  [switch]$Strict,
  [switch]$Pretty
)

$resolvedInput = [string]::IsNullOrWhiteSpace($InputPath) ? "" : $InputPath.Trim()

$cfg = $null
if (-not [string]::IsNullOrWhiteSpace($ConfigPath) -and (Test-Path -LiteralPath $ConfigPath)) {
  try {
    $cfg = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json
  }
  catch {
    Write-Warning "Failed to parse config at $ConfigPath. Falling back to inline defaults."
  }
}

if ($cfg -and $cfg.positiveFixture) {
  if ($InputPath -eq "docs/pdr/PDR-analytics-sample-events.ndjson" -and $cfg.positiveFixture.input) { $resolvedInput = [string]$cfg.positiveFixture.input }
  if ($SchemaVersion -eq "2026-06-06" -and $cfg.schemaVersion) { $SchemaVersion = [string]$cfg.schemaVersion }
  if ($Source -eq "howiezz-web" -and $cfg.source) { $Source = [string]$cfg.source }
  if ($MinTotalEvents -eq 8 -and $null -ne $cfg.positiveFixture.minTotalEvents) { $MinTotalEvents = [int]$cfg.positiveFixture.minTotalEvents }
  if ($MinPageViews -eq 2 -and $null -ne $cfg.positiveFixture.minPageViews) { $MinPageViews = [int]$cfg.positiveFixture.minPageViews }
  if ($MinCompareAdd -eq 1 -and $null -ne $cfg.positiveFixture.minCompareAdd) { $MinCompareAdd = [int]$cfg.positiveFixture.minCompareAdd }
  if ($MinInquiryAttempts -eq 1 -and $null -ne $cfg.positiveFixture.minInquiryAttempts) { $MinInquiryAttempts = [int]$cfg.positiveFixture.minInquiryAttempts }
  if ($MinAttributionCoverage -eq 0.8 -and $null -ne $cfg.positiveFixture.minAttributionCoverage) { $MinAttributionCoverage = [double]$cfg.positiveFixture.minAttributionCoverage }
}

if ($MinAttributionCoverage -lt 0 -or $MinAttributionCoverage -gt 1) {
  Write-Error "MinAttributionCoverage must be between 0 and 1."
  exit 2
}

if ($resolvedInput -eq "." -or $resolvedInput -eq "./" -or $resolvedInput -eq ".\\") {
  Write-Error "InputPath cannot be a placeholder path like '.'"
  exit 2
}

if (-not (Test-Path -LiteralPath $resolvedInput)) {
  Write-Error "InputPath does not exist: $resolvedInput"
  exit 2
}

$cmd = @(
  "scripts/analytics_event_sanity.py",
  "--input", $resolvedInput,
  "--schema-version", $SchemaVersion,
  "--source", $Source,
  "--min-total-events", "$MinTotalEvents",
  "--min-page-views", "$MinPageViews",
  "--min-compare-add", "$MinCompareAdd",
  "--min-inquiry-attempts", "$MinInquiryAttempts",
  "--min-attribution-coverage", "$MinAttributionCoverage"
)

if ($Strict) { $cmd += "--strict" }
if ($Pretty) { $cmd += "--pretty" }
if (-not [string]::IsNullOrWhiteSpace($OutputJson)) {
  $cmd += "--output-json"
  $cmd += $OutputJson.Trim()
}

Write-Host "Running analytics sanity checker..."
Write-Host ("python " + ($cmd -join " "))

python @cmd
$exit = $LASTEXITCODE
if ($exit -ne 0) {
  Write-Error "Analytics sanity checker failed with exit code $exit"
  exit $exit
}

Write-Host "Analytics sanity checker passed."
exit 0
