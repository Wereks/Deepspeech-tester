import toml
from pathlib import Path

def load(loc: Path) -> dict:
    return toml.load(path(loc))

def save(loc: Path, data):
    path(loc).write_text(toml.dumps(data))

def path(loc: Path):
    return loc.joinpath('tags.toml')