import json
from pathlib import Path

def load(loc: Path) -> dict:
    return json.loads(path(loc).read_text())

def save(loc: Path, data):
    path(loc).write_text(json.dumps(data))

def path(loc: Path) -> Path:
    return loc.joinpath('result.json')