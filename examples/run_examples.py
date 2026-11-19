#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
expected = (ROOT / "examples" / "output.json").read_text(encoding="utf-8")
result = subprocess.run([sys.executable, str(ROOT / "mcp_tool_surface_diff.py")],
    input=(ROOT / "examples" / "input.json").read_text(encoding="utf-8"), text=True,
    capture_output=True, cwd=ROOT, timeout=10)
if result.returncode != 0 or result.stdout != expected or result.stderr:
    sys.stderr.write("example output mismatch\n")
    raise SystemExit(1)
print("example: ok")
