import configparser
import toml
import pathlib


def init(config):
    global base_tags, module, scorer

    module = config.module
    scorer = config.scorer
    base_tags = config.base_tags


def load_expected_values(file_loc):
    """Czyta i konwertuje plik tekstowy z oczekiwanymi wynikami translacji

    :param file_loc: The file location
    :type file_loc: str
    :returns: dict, where keys are the audio file names and values the expected translation
    :rtype: dict
    """

    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(file_loc)

    result = {}
    for (wav_name, section) in parser.items():
        if wav_name != parser.default_section:
            expected_output = ' '.join(section.keys()).strip()
            result[wav_name] = expected_output

    return result

def save_expected_values(loc, data):
    lines = []
    for file_name, expected_output in data.items():
        lines.extend([f"[{file_name}]", expected_output])
    lines = "\n".join(lines)

    loc.joinpath('expected', 'w').write_text(lines)


def save_tags_value(loc, code = None, tags = None):
    #TODO
    tags_from_code = decipher_tags(code) if code is not None else None
    code_from_tags = encrypt_tags(tags) if tags is not None else None


def decipher_tags(code):
    """Zamienia kod liczbowy na tagi

    :param code: code which defines used tags
    :type code: str
    :param tags: dict with keys as tag category and values as tag name
    :type tags: dict

    :raises ValueError: when the type of the tag isn't bool or list

    :returns: dict, where keys are tag category and value is the tag name
    :rtype: dict
    """

    result = {}
    for num, (category_name, category) in zip(code, base_tags.items()):
        if isinstance(category, list):
            result[category_name] = category[num]
        elif isinstance(category, bool):
            result[category_name] = False if num == 0 else True
        else:
            raise ValueError("Nie przewidziano innego typu taga")

    return result

def encrypt_tags(source):
    """Zamienia kod liczbowy na tagi

    :param source: dict with string keys as tag category and values as string tag name
    :type source: dict
    :param tags: dict with keys as tag category and values as tag name
    :type tags: dict

    :raises ValueError: when the tag doesnt exists in both and when the type of the tag isn't bool or list

    :returns: code which identifies the tags
    :rtype: str
    """
    result = []

    for (category_name, category) in base_tags.items():
        if category_name not in source:
            raise ValueError("Nie znaleziono kategorii")

        num = -1
        if isinstance(category, list):
            num = category.index(source['category_name'])
        elif isinstance(category, bool):
            num = 1 if source['category_name'] else 0
        else:
            raise ValueError("Nie przewidziano innego typu taga")

        result.append(num)

    return ''.join(result)