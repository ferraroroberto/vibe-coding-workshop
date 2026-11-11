#Requires -Version 5.1
<#
.SYNOPSIS
    Pre-ship verification gate for vibe-coding-workshop.

.DESCRIPTION
    The repo has no test suite, so the gate is nine ratchets. The structure ratchet,
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
    creationflags (no-window), a hardcoded drive path (no-drive-path) or a blocking
    spawn without timeout= (subprocess-timeout) beyond
    .conventions-ratchet-baseline.json. The runtime write ratchet,
    scripts/runtime_write_ratchet.py, fails when a Python file gains a write target
    that resolves under a code folder beyond .runtime-write-ratchet-baseline.json; a
    new target it cannot resolve is exit 3. With no test stage there is nothing for its
    --snapshot/--probe bracket to surround, so only the static half runs. The last stage,
    scripts/validate_exercises.py, runs every exercise's setup script then its solution and
    fails the gate if any of them exits non-zero. Each ratchet is opt-in via its .fleet.toml table. Exit 3 means
    "not confirmed" (git unusable, an unparseable file) and fails the gate, never
    passes it.

    Run from anywhere:  & .\scripts\verify-before-ship.ps1

    Verdict line: the last line on stdout is `GATE-RESULT: PASS` or
    `GATE-RESULT: FAIL`, on every path that can still run code. Never pipe the
    gate when its exit code matters (a pipeline reports its last command's
    status, so `... | tail -40` turns a red run green); a caller that cannot
    avoid a pipe asserts on that line. A run with no such line is not a pass.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# gate-verdict:begin
# The verdict is the last stdout line of every path that can still run code. A
# terminating error under the "Stop" preference above would otherwise print to
# stderr only and exit 1, leaving a piped caller an empty, apparently clean run,
# so the trap reports it on stdout first. A stage's own exit code (including 3,
# "not confirmed") is the gate's exit code; any non-zero code prints FAIL.
function Write-GateResult($verdict) {
    Write-Host "GATE-RESULT: $verdict"
}

function Complete-Gate([int]$Code) {
    Write-GateResult $(if ($Code -eq 0) { "PASS" } else { "FAIL" })
    exit $Code
}

trap {
    Write-Host ""
    Write-Host "[FAIL] the gate aborted on an unhandled error:" -ForegroundColor Red
    Write-Host ("       {0}" -f $_.Exception.Message) -ForegroundColor Red
    Complete-Gate 1
}

function Invoke-Stage {
    param([string]$Name, [scriptblock]$Body)
    Write-Host "==> $Name" -ForegroundColor Cyan
    & $Body
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        if ($code -eq 3) {
            Write-Host "[FAIL] ${Name}: NOT CONFIRMED (exit 3) - counts as a failure" -ForegroundColor Red
        } else {
            Write-Host "[FAIL] $Name failed (exit $code)" -ForegroundColor Red
        }
        Complete-Gate $code
    }
}
# gate-verdict:end

Set-Location (Join-Path $PSScriptRoot "..")

$py = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "[FAIL] .venv not found at $py" -ForegroundColor Red
    Write-Host "       Create it and run: $py -m pip install -r requirements.txt" -ForegroundColor Red
    Complete-Gate 1
}

$stages = @(
    @{ Name = "structure ratchet";   Script = "scripts/structure_ratchet.py" },
    @{ Name = "instruction ratchet"; Script = "scripts/instruction_ratchet.py" },
    @{ Name = "doc refs ratchet";    Script = "scripts/doc_refs_ratchet.py" },
    @{ Name = "dead code ratchet";   Script = "scripts/dead_code_ratchet.py" },
    @{ Name = "static ratchet";      Script = "scripts/static_ratchet.py" },
    @{ Name = "docs ratchet";        Script = "scripts/docs_ratchet.py" },
    @{ Name = "comment ratchet";     Script = "scripts/comment_ratchet.py" },
    @{ Name = "conventions ratchet"; Script = "scripts/conventions_ratchet.py" },
    @{ Name = "runtime write ratchet"; Script = "scripts/runtime_write_ratchet.py" },
    @{ Name = "gate verdict test";   Script = "scripts/test_gate_result.py" },
    @{ Name = "exercise validation"; Script = "scripts/validate_exercises.py" }
)

foreach ($stage in $stages) {
    $script = $stage.Script
    Invoke-Stage $stage.Name { & $py $script }
}

Write-Host "[OK] verify-before-ship passed" -ForegroundColor Green
Complete-Gate 0
