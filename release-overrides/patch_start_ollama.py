from __future__ import annotations

from pathlib import Path
import sys

OLD = '''    for app in ("LocalAI", "Ollama"):\n        failed = subprocess.run(["open", "-a", app], check=False).returncode != 0 or failed\n'''

NEW = '''    failed = subprocess.run(["open", "-a", "LocalAI"], check=False).returncode != 0 or failed\n\n    ollama = shutil.which("ollama")\n    if ollama:\n        ollama_ready = subprocess.run(\n            [ollama, "ps"],\n            stdout=subprocess.DEVNULL,\n            stderr=subprocess.DEVNULL,\n            check=False,\n        ).returncode == 0\n        if not ollama_ready:\n            subprocess.Popen(\n                [ollama, "serve"],\n                stdout=subprocess.DEVNULL,\n                stderr=subprocess.DEVNULL,\n                start_new_session=True,\n            )\n            for _ in range(30):\n                if subprocess.run(\n                    [ollama, "ps"],\n                    stdout=subprocess.DEVNULL,\n                    stderr=subprocess.DEVNULL,\n                    check=False,\n                ).returncode == 0:\n                    ollama_ready = True\n                    break\n                time.sleep(1)\n        failed = (not ollama_ready) or failed\n    else:\n        ollama_app_exists = subprocess.run(\n            ["open", "-Ra", "Ollama"],\n            stdout=subprocess.DEVNULL,\n            stderr=subprocess.DEVNULL,\n            check=False,\n        ).returncode == 0\n        if ollama_app_exists:\n            failed = subprocess.run(["open", "-a", "Ollama"], check=False).returncode != 0 or failed\n        else:\n            failed = True\n'''


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'ollama = shutil.which("ollama")' in text:
        return False
    if OLD not in text:
        raise RuntimeError("expected Ollama app-only start block was not found")
    if "import time\n" not in text:
        marker = "import subprocess\n"
        if marker not in text:
            raise RuntimeError("expected subprocess import was not found")
        text = text.replace(marker, marker + "import time\n", 1)
    text = text.replace(OLD, NEW, 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch_start_ollama.py PATH", file=sys.stderr)
        return 2
    changed = patch_file(Path(sys.argv[1]))
    print("patched" if changed else "already-patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
