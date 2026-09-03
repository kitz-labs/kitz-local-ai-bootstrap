from __future__ import annotations

import argparse
from pathlib import Path

OLD = 'timeout: float = 30.0,'
NEW = 'timeout: float = 240.0,'


def patch_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if NEW in text:
        return f'{path}: already patched'
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(
            f'{path}: expected exactly one default LocalAI timeout marker, found {count}'
        )
    path.write_text(text.replace(OLD, NEW, 1), encoding='utf-8')
    return f'{path}: patched 30s -> 240s'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args()

    seen: set[Path] = set()
    for raw in args.paths:
        path = raw.expanduser().resolve()
        if path in seen:
            continue
        seen.add(path)
        if not path.is_file():
            raise FileNotFoundError(path)
        print(patch_file(path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
