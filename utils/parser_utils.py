import subprocess, sys
from pathlib import Path

def save_parser(bank, code):
    path = Path(f"custom_parsers/{bank}_parser.py")
    path.parent.mkdir(exist_ok=True)
    path.write_text(code, encoding="utf-8")
    return path

def test_parser(bank):
    try:
        cmd = [sys.executable, "-m", "pytest", f"tests/test_parser.py::test_{bank}", "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print("Test failed:", e)
        return False
