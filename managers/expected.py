from configparser import ConfigParser
from pathlib import Path

from .iop import expected

class ExpectedManager():
    def load(self, loc: Path) -> dict[str,str]:
        parser = ConfigParser(allow_no_value=True)
        parser.read(self.path(loc))

        result = {}
        for (wav_name, section) in parser.items():
            if wav_name != parser.default_section:
                expected_output = ' '.join(section.keys()).strip()
                result[wav_name] = expected_output

        return result

    def save(self, loc: Path, data):
        lines = []
        for file_name, expected_output in data.items():
            lines.extend([f"[{file_name}]", expected_output])
        lines = "\n".join(lines)

        self.path(loc).write_text(lines)

    def path(self, loc: Path):
        return loc.joinpath('expected.txt')