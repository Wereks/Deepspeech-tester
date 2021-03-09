import configparser
from abc import ABC, abstractmethod
from functools import singledispatch
from pathlib import Path

import toml


class Resources(ABC):
    @abstractmethod
    def load(self, loc: Path):
        pass

    @abstractmethod
    def save(self, loc: Path, data):
        pass


class ExpectedResource(Resources):
    def load(self, loc: Path) -> dict[str,str]:
        """Czyta i konwertuje plik tekstowy z oczekiwanymi wynikami translacji"""

        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(loc)

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

        loc.joinpath('expected', 'w').write_text(lines)


class TagResource(Resources):
    base_tags : dict[str, str]

    def __init__(self, base_tags):
        self.base_tags = base_tags


    def load(self, loc: Path) -> dict:
        with loc.open('r') as f:
            nonlocal conf
            conf = toml.load(f)
    
        #TODO: Checking if code and tags are the same
        (code, tags) = self.code_tags(conf.get('code', conf.get('tags')))

        return {
                'code': code,
                'tags': tags
                }
   
    def save(self, loc: Path, data):
        (code, tags) = self.code_tags(data)

        with loc.open('w') as f:
            toml.dump({'code': code, 'tags': tags}, f)
        



    @singledispatch 
    def code_tags(self, source) -> (str, dict[str,str]):
        raise TypeError("Source is invalid, can't generate pair (code, tags)")

    @code_tags.register(str)
    def decipher_tags(self, code: str) -> dict[str,str]:

        result = {}
        for num, (category_name, category) in zip(code, self.base_tags.items()):
            if isinstance(category, list):
                result[category_name] = category[num]
            elif isinstance(category, bool):
                result[category_name] = False if num == 0 else True
            else:
                raise ValueError("Nie przewidziano innego typu taga")

        return result

    @code_tags.register(list)
    def encrypt_tags(self, source : dict[str, str]) -> str:

        if (a := set(self.base_tags.keys())) != (b := set(source.keys())):
            raise ValueError(f"""Base tags don't match the source tags:
                                In base but not in source: {a - b}
                                In source but not in base: {b - a}"""
                            )
        
        result = []
        for (category_name, category) in self.base_tags.items():
            tag = source.get(category_name)

            if isinstance(category, list):
                num = category.index(tag)
                result.append(num)
            elif isinstance(category, bool):
                num = 1 if tag else 0
                result.append(num)
            else:
                raise TypeError(f"{category_name} must be bool or list, but was {type(category)}")


        return ''.join(result)

