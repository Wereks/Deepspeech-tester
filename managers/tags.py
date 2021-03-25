import toml
from pathlib import Path
from functools import singledispatchmethod

from .iop import tags


class TagManager():
    base_tags : dict

    def __init__(self, base_tags : dict):
        self.base_tags = base_tags

    def load(self, loc: Path):
        conf = tags.load(loc)
    
        (code, tags_dict) = self.code_tags(conf.get('code') or conf.get('tags'))

        return {
                'code': code,
                'tags': tags_dict
                }

    def save(self, loc: Path, code = None, tags_dict = None):
        (code, tags_dict) = self.code_tags(code)
        tags.save(loc, {
                'code': code,
                'tags': tags_dict
        })

    def categories(self):
        return self.base_tags.keys()

    def tags_dict(self, code):
        (_, tags_dict) = self.code_tags(code)
        return tags_dict


    def load_code(self, loc):
        return self.load(loc)['code']



    @singledispatchmethod
    def code_tags(self, source) -> (str, dict[str]):
        raise TypeError("Source is invalid, can't generate pair (code, tags)")

    @code_tags.register(str)
    def decipher_tags(self, code) -> dict[str]:

        result = {}
        for num, (category_name, category) in zip(code, self.base_tags.items()):
            if isinstance(category, list):
                result[category_name] = category[int(num)]
            elif isinstance(category, bool):
                result[category_name] = False if num == '0' else True
            else:
                raise ValueError("Nie przewidziano innego typu taga")

        return (code, result)

    @code_tags.register(dict)
    def encrypt_tags(self, source : dict[str]) -> str:

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


        return (''.join(result), source)



