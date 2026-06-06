Write-Host "Running analytics CI parity checks..."

$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host "[1/3] Baseline suite (expected pass)"
pwsh -File (Join-Path $repoRoot "scripts/run_analytics_sanity_suite.ps1")
if ($LASTEXITCODE -ne 0) {
  Write-Error "Baseline analytics sanity suite failed unexpectedly"
  exit $LASTEXITCODE
}

Write-Host "[2/3] Invalid threshold config (expected exit 2)"
pwsh -File (Join-Path $repoRoot "scripts/run_analytics_sanity_suite.ps1") -ConfigPath "docs/pdr/PDR-analytics-sanity-thresholds.invalid.json"
if ($LASTEXITCODE -ne 2) {
  Write-Error "Expected exit code 2 for invalid-threshold config, got $LASTEXITCODE"
  exit 1
}

Write-Host "[3/3] Missing keys config (expected exit 2)"
pwsh -File (Join-Path $repoRoot "scripts/run_analytics_sanity_suite.ps1") -ConfigPath "docs/pdr/PDR-analytics-sanity-thresholds.missing-keys.json"
if ($LASTEXITCODE -ne 2) {
  Write-Error "Expected exit code 2 for missing-keys config, got $LASTEXITCODE"
  exit 1
}

Write-Host "Analytics CI parity checks passed."
exit 0
