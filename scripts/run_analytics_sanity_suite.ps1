Param(
  [string]$ConfigPath = "docs/pdr/PDR-analytics-sanity-thresholds.json"
)

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
  },
  "negativeFixtures": {
    "broken": { "input": "docs/pdr/PDR-analytics-sample-events-broken.ndjson" },
    "lowAttribution": {
      "input": "docs/pdr/PDR-analytics-sample-events-low-attribution.ndjson",
      "minAttributionCoverage": 0.8
    }
  }
}
#>

Write-Host "Running analytics sanity suite..."

$repoRoot = Split-Path -Parent $PSScriptRoot
$artifactDir = Join-Path $repoRoot ".artifacts/analytics"
New-Item -ItemType Directory -Force -Path $artifactDir | Out-Null

$resolvedConfig = [string]::IsNullOrWhiteSpace($ConfigPath) ? "" : $ConfigPath.Trim()
if ($resolvedConfig -eq "." -or $resolvedConfig -eq "./" -or $resolvedConfig -eq ".\\") {
  Write-Error "ConfigPath cannot be a placeholder path like '.'"
  exit 2
}

$configPath = if ([System.IO.Path]::IsPathRooted($resolvedConfig)) { $resolvedConfig } else { Join-Path $repoRoot $resolvedConfig }
if (-not (Test-Path -LiteralPath $configPath)) {
  Write-Error "Missing config file: $configPath"
  exit 2
}

Write-Host "Analytics config path: $configPath"

try {
  $cfg = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
}
catch {
  Write-Error "Failed to parse config file: $configPath"
  exit 2
}

if (-not $cfg.positiveFixture -or -not $cfg.negativeFixtures) {
  Write-Error "Config file missing required sections: positiveFixture/negativeFixtures"
  exit 2
}

if (-not $cfg.positiveFixture.input -or -not $cfg.negativeFixtures.broken.input -or -not $cfg.negativeFixtures.lowAttribution.input) {
  Write-Error "Config file missing required fixture input paths."
  exit 2
}

$schemaVersion = if ($cfg.schemaVersion) { [string]$cfg.schemaVersion } else { "2026-06-06" }
$source = if ($cfg.source) { [string]$cfg.source } else { "howiezz-web" }

Write-Host "Analytics config schema_version: $schemaVersion"
Write-Host "Analytics config source: $source"

$positiveInput = [string]$cfg.positiveFixture.input
$brokenInput = [string]$cfg.negativeFixtures.broken.input
$lowAttrInput = [string]$cfg.negativeFixtures.lowAttribution.input

$minTotalEvents = [int]$cfg.positiveFixture.minTotalEvents
$minPageViews = [int]$cfg.positiveFixture.minPageViews
$minCompareAdd = [int]$cfg.positiveFixture.minCompareAdd
$minInquiryAttempts = [int]$cfg.positiveFixture.minInquiryAttempts
$minAttributionCoverage = [double]$cfg.positiveFixture.minAttributionCoverage
$lowAttrThreshold = if ($null -ne $cfg.negativeFixtures.lowAttribution.minAttributionCoverage) { [double]$cfg.negativeFixtures.lowAttribution.minAttributionCoverage } else { $minAttributionCoverage }

if ($minAttributionCoverage -lt 0 -or $minAttributionCoverage -gt 1 -or $lowAttrThreshold -lt 0 -or $lowAttrThreshold -gt 1) {
  Write-Error "Attribution coverage thresholds must be between 0 and 1."
  exit 2
}

$positiveArgs = @(
  "scripts/analytics_event_sanity.py",
  "--input", $positiveInput,
  "--schema-version", $schemaVersion,
  "--source", $source,
  "--strict",
  "--min-total-events", "$minTotalEvents",
  "--min-page-views", "$minPageViews",
  "--min-compare-add", "$minCompareAdd",
  "--min-inquiry-attempts", "$minInquiryAttempts",
  "--min-attribution-coverage", "$minAttributionCoverage",
  "--output-json", (Join-Path $artifactDir "positive-summary.local.json")
)

Write-Host "[1/3] Positive fixture (expected pass)"
python @positiveArgs
if ($LASTEXITCODE -ne 0) {
  Write-Error "Positive fixture failed unexpectedly"
  exit $LASTEXITCODE
}

$brokenSchemaArgs = @(
  "scripts/analytics_event_sanity.py",
  "--input", $brokenInput,
  "--schema-version", $schemaVersion,
  "--source", $source,
  "--strict",
  "--output-json", (Join-Path $artifactDir "broken-summary.local.json")
)

Write-Host "[2/3] Broken schema fixture (expected fail)"
python @brokenSchemaArgs
if ($LASTEXITCODE -eq 0) {
  Write-Error "Broken schema fixture passed unexpectedly"
  exit 1
}

$lowAttrArgs = @(
  "scripts/analytics_event_sanity.py",
  "--input", $lowAttrInput,
  "--schema-version", $schemaVersion,
  "--source", $source,
  "--strict",
  "--min-attribution-coverage", "$lowAttrThreshold",
  "--output-json", (Join-Path $artifactDir "low-attribution-summary.local.json")
)

Write-Host "[3/3] Low attribution fixture (expected fail)"
python @lowAttrArgs
if ($LASTEXITCODE -eq 0) {
  Write-Error "Low attribution fixture passed unexpectedly"
  exit 1
}

Write-Host "Analytics sanity suite passed (expected pass/fail behavior confirmed)."
exit 0
