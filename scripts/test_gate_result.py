"""The pre-ship gate ends every run with a `GATE-RESULT: PASS|FAIL` stdout line.

A pipeline reports its last command's status, so `verify-before-ship.ps1 | tail`
hands the caller `tail`'s 0 and a red gate reads green. The verdict line is the
part a pipe cannot rewrite. The helper block in the gate (between the
`gate-verdict` markers) is run for real, over a captured stdout (the same
anonymous pipe `|` creates), for a pass, a failed stage and an early terminating
error; the real script is run for the paths that need no stage to execute.

Standard library only (the repo has no pytest). Run from the repo root:
    .\\.venv\\Scripts\\python.exe scripts\\test_gate_result.py
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE = REPO_ROOT / "scripts" / "verify-before-ship.ps1"
POWERSHELL = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"

windows_only = unittest.skipUnless(sys.platform == "win32", "the gate is a Windows PowerShell script")


def _verdict_block() -> str:
    text = GATE.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.search(r"# gate-verdict:begin\n(.*?)# gate-verdict:end", text, re.DOTALL)
    assert match, "the gate lost its gate-verdict block"
    return match.group(1)


def _run(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(POWERSHELL), "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW, timeout=120, env=env,
    )


def _run_scenario(scenario: str) -> subprocess.CompletedProcess[str]:
    script = f'$ErrorActionPreference = "Stop"\n{_verdict_block()}\n{scenario}\n'
    return _run(["-Command", script])


def _last_line(run: subprocess.CompletedProcess[str]) -> str:
    lines = [line.rstrip() for line in run.stdout.splitlines() if line.strip()]
    assert lines, f"nothing on stdout; stderr={run.stderr!r}"
    return lines[-1]


class GateResultTest(unittest.TestCase):
    @windows_only
    def test_pass_ends_with_pass_and_exits_zero(self) -> None:
        run = _run_scenario('Invoke-Stage "ok" { cmd /c exit 0 }\nComplete-Gate 0')
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: PASS")

    @windows_only
    def test_failed_stage_ends_with_fail_and_keeps_the_stage_exit_code(self) -> None:
        run = _run_scenario('Invoke-Stage "bad" { cmd /c exit 7 }\nComplete-Gate 0')
        self.assertEqual(run.returncode, 7, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: FAIL")
        self.assertIn("[FAIL] bad failed (exit 7)", run.stdout)

    @windows_only
    def test_not_confirmed_stage_ends_with_fail_and_exits_three(self) -> None:
        run = _run_scenario('Invoke-Stage "unsure" { cmd /c exit 3 }\nComplete-Gate 0')
        self.assertEqual(run.returncode, 3, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: FAIL")
        self.assertIn("NOT CONFIRMED", run.stdout)

    @windows_only
    def test_early_terminating_error_reports_on_stdout_then_fails(self) -> None:
        run = _run_scenario('throw "boom before any stage"')
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: FAIL")
        self.assertIn("boom before any stage", run.stdout, "the error must reach stdout, not only stderr")

    @windows_only
    def test_missing_venv_ends_with_fail_and_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = _run(["-File", str(_gate_copy(Path(tmp)))])
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: FAIL")
        self.assertIn(".venv not found", run.stdout)

    @windows_only
    def test_unrunnable_interpreter_is_reported_as_fail_not_a_silent_run(self) -> None:
        """A terminating error in the real script: the interpreter path exists but is not an executable."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gate = _gate_copy(root)
            interpreter = root / ".venv" / "Scripts" / "python.exe"
            interpreter.parent.mkdir(parents=True)
            interpreter.write_text("not an executable", encoding="utf-8")
            run = _run(["-File", str(gate)])
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertEqual(_last_line(run), "GATE-RESULT: FAIL")

    def test_every_exit_goes_through_the_verdict(self) -> None:
        """A new `exit` that skips `Complete-Gate` would end a run with no verdict."""
        text = GATE.read_text(encoding="utf-8").replace("\r\n", "\n")
        outside = text.replace(_verdict_block(), "")
        self.assertIsNone(re.search(r"^\s*exit\s+\S", outside, re.MULTILINE), "exit through Complete-Gate, not directly")
        self.assertTrue(text.rstrip().endswith("Complete-Gate 0"), "the pass path must end on its verdict")

    def test_verdict_block_is_ascii_for_windows_powershell_5_1(self) -> None:
        """Windows PowerShell 5.1 reads a BOM-less file as ANSI, so the block stays ASCII."""
        _verdict_block().encode("ascii")


def _gate_copy(root: Path) -> Path:
    scripts = root / "scripts"
    scripts.mkdir()
    shutil.copy2(GATE, scripts / GATE.name)
    return scripts / GATE.name


if __name__ == "__main__":
    unittest.main()
