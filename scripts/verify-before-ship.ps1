#Requires -Version 5.1
<#
.SYNOPSIS
    Pre-ship verification gate for vibe-coding-workshop.

.DESCRIPTION
    The repo has no test suite, so the gate is eight ratchets. The structure ratchet,
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
    dated headings or changelog headings beyond .docs-ratchet-baseline.json. The comment ratchet, scripts/comment_ratchet.py, fails
    when a file gains issue references (#NNN) in its Python, JS, CSS or PowerShell comments
    beyond .comment-ratchet-baseline.json. The conventions ratchet,
    scripts/conventions_ratchet.py, fails when a Python file gains a spawn without
    creationflags (no-window) or a hardcoded drive path (no-drive-path) beyond
    .conventions-ratchet-baseline.json. Each is opt-in via its .fleet.toml table. Exit 3 means
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

$stages = @(
    @{ Name = "structure ratchet";   Script = "scripts/structure_ratchet.py" },
    @{ Name = "instruction ratchet"; Script = "scripts/instruction_ratchet.py" },
    @{ Name = "doc refs ratchet";    Script = "scripts/doc_refs_ratchet.py" },
    @{ Name = "dead code ratchet";   Script = "scripts/dead_code_ratchet.py" },
    @{ Name = "static ratchet";      Script = "scripts/static_ratchet.py" },
    @{ Name = "docs ratchet";        Script = "scripts/docs_ratchet.py" },
    @{ Name = "comment ratchet";     Script = "scripts/comment_ratchet.py" },
    @{ Name = "conventions ratchet"; Script = "scripts/conventions_ratchet.py" }
)

foreach ($stage in $stages) {
    Write-Host "==> $($stage.Name)" -ForegroundColor Cyan
    & $py $stage.Script
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        if ($code -eq 3) {
            Write-Host "[FAIL] $($stage.Name): NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
        } else {
            Write-Host "[FAIL] $($stage.Name) failed (exit $code)" -ForegroundColor Red
        }
        exit $code
    }
}

Write-Host "[OK] verify-before-ship passed" -ForegroundColor Green
