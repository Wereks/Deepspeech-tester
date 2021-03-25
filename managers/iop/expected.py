from configparser import ConfigParser
from pathlib import Path

def load(loc: Path) -> dict[str,str]:
    parser = ConfigParser(allow_no_value=True)
    parser.read(path(loc))

    result = {}
    for (wav_name, section) in parser.items():
        if wav_name != parser.default_section:
            expected_output = ' '.join(section.keys()).strip()
            result[wav_name] = expected_output

    return result

def save(loc: Path, data):
    lines = []
    for file_name, expected_output in data.items():
        lines.extend([f"[{file_name}]", expected_output])
    lines = "\n".join(lines)

    path(loc).write_text(lines)

def path(loc: Path):
    return loc.joinpath('expected.txt')