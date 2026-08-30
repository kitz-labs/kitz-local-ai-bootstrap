from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path

MODEL_NAME = 'kitz-agent'
BACKEND_NAME = 'kitz-native'
AGENT_CORE_HEALTH_URL = 'http://127.0.0.1:8787/health'


def render_model_config() -> str:
    return (
        'name: kitz-agent\n'
        'description: KITZ Agent Core - native LocalAI gRPC backend\n'
        'known_usecases:\n'
        '  - chat\n'
        'backend: kitz-native\n'
        'parameters:\n'
        '  model: kitz-agent\n'
        'pii:\n'
        '  enabled: false\n'
    )


def upsert_external_backend_env(env_path: Path, run_path: Path) -> None:
    env_path = Path(env_path).expanduser()
    env_path.parent.mkdir(parents=True, exist_ok=True)
    line = f'LOCALAI_EXTERNAL_GRPC_BACKENDS={BACKEND_NAME}:{run_path}\n'
    existing = env_path.read_text(encoding='utf-8').splitlines(keepends=True) if env_path.exists() else []
    out = []
    replaced = False
    for old in existing:
        if old.startswith('LOCALAI_EXTERNAL_GRPC_BACKENDS=') or old.startswith('EXTERNAL_GRPC_BACKENDS='):
            if not replaced:
                out.append(line)
                replaced = True
        else:
            out.append(old)
    if not replaced:
        out.append(line)
    env_path.write_text(''.join(out), encoding='utf-8')


def find_proto_source(backends_root: Path, target_dir: Path) -> Path:
    candidates = []
    for pb2 in backends_root.rglob('backend_pb2.py'):
        if target_dir in pb2.parents:
            continue
        if (pb2.parent / 'backend_pb2_grpc.py').exists():
            candidates.append(pb2.parent)
    if not candidates:
        raise RuntimeError('No installed LocalAI Python backend with backend_pb2.py found')
    return sorted(candidates, key=lambda p: ('mlx' not in str(p).lower(), len(str(p))))[0]


def write_atomic(path: Path, text: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def backup_model_config(model_path: Path) -> Path | None:
    if not model_path.exists():
        return None
    backup_dir = model_path.parent.parent / 'backups' / MODEL_NAME
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = backup_dir / f'{model_path.name}.pre-v1.1.0-{stamp}'
    shutil.copy2(model_path, backup)
    return backup


def ensure_venv(backend_dir: Path) -> None:
    uv = shutil.which('uv')
    if not uv:
        raise RuntimeError('uv is required')
    venv = backend_dir / 'venv'
    if not (venv / 'bin' / 'python').exists():
        subprocess.run([uv, 'venv', '--python', '3.12', str(venv)], check=True)
    env = dict(os.environ)
    env['VIRTUAL_ENV'] = str(venv)
    subprocess.run([uv, 'pip', 'install', 'grpcio>=1.66,<2', 'protobuf>=5,<7'], env=env, check=True)


def install_backend(backend_source: Path, home: Path) -> Path:
    localai_root = home / '.localai'
    backends_root = Path(os.environ.get('LOCALAI_BACKENDS_PATH', localai_root / 'backends')).expanduser()
    backend_dir = backends_root / BACKEND_NAME
    backend_dir.mkdir(parents=True, exist_ok=True)
    proto_source = find_proto_source(backends_root, backend_dir)
    shutil.copy2(proto_source / 'backend_pb2.py', backend_dir / 'backend_pb2.py')
    shutil.copy2(proto_source / 'backend_pb2_grpc.py', backend_dir / 'backend_pb2_grpc.py')
    shutil.copy2(backend_source, backend_dir / 'backend.py')
    ensure_venv(backend_dir)
    run_path = backend_dir / 'run.sh'
    write_atomic(
        run_path,
        '#!/usr/bin/env bash\nset -euo pipefail\nDIR="$(cd "$(dirname "$0")" && pwd)"\nexec "$DIR/venv/bin/python" "$DIR/backend.py" "$@"\n',
        0o755,
    )
    return run_path


def verify_agent_core() -> None:
    with urllib.request.urlopen(AGENT_CORE_HEALTH_URL, timeout=5) as resp:
        if resp.status != 200:
            raise RuntimeError(f'Agent Core health HTTP {resp.status}')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend-source', type=Path, required=True)
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args(argv)
    home = args.home.expanduser()
    verify_agent_core()
    run_path = install_backend(args.backend_source, home)
    models_dir = Path(os.environ.get('LOCALAI_MODELS_PATH', home / '.localai' / 'models')).expanduser()
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / f'{MODEL_NAME}.yaml'
    backup = backup_model_config(model_path)
    write_atomic(model_path, render_model_config())
    env_path = home / '.config' / 'localai.env'
    upsert_external_backend_env(env_path, run_path)
    print(f'[native] backend: {run_path}')
    print(f'[native] model config: {model_path}')
    print(f'[native] LocalAI env: {env_path}')
    if backup:
        print(f'[native] backup: {backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
