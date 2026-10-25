#Requires -Version 5.1
<#
.SYNOPSIS
    Pre-ship verification gate for vibe-coding-workshop.

.DESCRIPTION
    The repo has no test suite, so the gate is six ratchets. The structure ratchet,
    scripts/structure_ratchet.py, fails when a new file passes 1,000 lines, a new
    function 100 lines or a flat directory 40 modules, and when a baselined
    offender grows past its size in .structure-ratchet-baseline.json. The
    instruction ratchet, scripts/instruction_ratchet.py, fails when a rule-hit count
    in CLAUDE.md or AGENTS.md rises above .instruction-ratchet-baseline.json or a
    file passes its size cap. The doc-refs ratchet, scripts/doc_refs_ratchet.py, fails
    when README.md, CLAUDE.md or docs/ names a path, module, link or port that does not
    exist beyond .doc-refs-ratchet-baseline.json. The dead-code ratchet,
    scripts/dead_code_ratchet.py, fails when a new Python function, class or method
    appears that nothing in the repo refers to, beyond .dead-code-ratchet-baseline.json.
    The static ratchet, scripts/static_ratchet.py, fails on a new duplicated block (jscpd
    through npx), unused import or variable, or likely-bug and security finding (ruff)
    beyond .static-ratchet-baseline.json. The docs ratchet, scripts/docs_ratchet.py, fails when
    the root README.md passes its size budget or README.md and docs/ gain issue references,
    dated headings or changelog headings beyond .docs-ratchet-baseline.json. Each is opt-in via its .fleet.toml table. Exit 3 means
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

Write-Host "==> doc refs ratchet" -ForegroundColor Cyan
& $py "scripts/doc_refs_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] doc refs ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] doc refs ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "==> dead code ratchet" -ForegroundColor Cyan
& $py "scripts/dead_code_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] dead code ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] dead code ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "==> static ratchet" -ForegroundColor Cyan
& $py "scripts/static_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] static ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] static ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "==> docs ratchet" -ForegroundColor Cyan
& $py "scripts/docs_ratchet.py"
$code = $LASTEXITCODE
if ($code -ne 0) {
    if ($code -eq 3) {
        Write-Host "[FAIL] docs ratchet: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] docs ratchet failed (exit $code)" -ForegroundColor Red
    }
    exit $code
}

Write-Host "[OK] verify-before-ship passed" -ForegroundColor Green
