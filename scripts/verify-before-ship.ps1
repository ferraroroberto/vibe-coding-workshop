#Requires -Version 5.1
<#
.SYNOPSIS
    Pre-ship verification gate for vibe-coding-workshop.

.DESCRIPTION
    The repo has no test suite, so the gate is two ratchets. The structure ratchet,
    scripts/structure_ratchet.py, fails when a new file passes 1,000 lines, a new
    function 100 lines or a flat directory 40 modules, and when a baselined
    offender grows past its size in .structure-ratchet-baseline.json. The
    instruction ratchet, scripts/instruction_ratchet.py, fails when a rule-hit count
    in CLAUDE.md or AGENTS.md rises above .instruction-ratchet-baseline.json or a
    file passes its size cap. Each is opt-in via its .fleet.toml table. Exit 3 means
    "not confirmed" (git unusable, an unparseable file) and fails the gate, never
    passes it.

    Run from anywhere:  & .\scripts\verify-before-ship.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$py = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "[FAIL] .venv not found at $py" -ForegroundColor Red
    Write-Host "       Create it and run: $py -m pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

Write-Host "==> structure ratchet" -ForegroundColor Cyan
& $py "scripts/structure_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] structure ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] structure ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "==> instruction ratchet" -ForegroundColor Cyan
& $py "scripts/instruction_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] instruction ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] instruction ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "[OK] verify-before-ship passed" -ForegroundColor Green
