from pathlib import Path
from collections import defaultdict
import csv

import toml

from managers import ExpectedManager, ResultManager, TagManager
import ds

def _zip_dicts(*dcts):
    if not dcts:
        return
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield (i,) + tuple(d[i] for d in dcts)


def _save_to_csv(dct):
    with open('result.csv', 'w', newline='') as csv_file:
        field_names = list(tagManager.categories()) + list(resultManager.categories())
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        for code, result_list in dct.items():
            tags_dict = tagManager.tags_dict(code)
            for result in result_list:
                writer.writerow(tags_dict | resultManager.calculate_whole(result))


def _get_audio_files(loc: Path) -> dict[str]:
    return [path for path in loc.glob('./audio/*.wav') if path.is_file()]

def _cases(name=None):
    if name:
        return [Path(f'./workspace/{name}')]
    
    return Path('./workspace').iterdir()


def repair(args):
    #Sprawdz czy istnieje result.txt
    #Sprawdz czy tags.txt ma w swobie kod i poprawne tagi do kodu
    #Wrzuc wszystkie pliki .wav do folderu audio
    #Sprawdz czy kazdy audio_file ma swoj niepusty expected WPP dopisz kolumny
    pass

def transcript(args):
    for case in _cases(args.name):
        audio_files = _get_audio_files(case)
        audio_trascriptions = {path.stem : ds.transcript(path) for path in audio_files}

        expected = expectedManager.load(case)

        result = {name : resultManager.calculate(actual, exp) for (name, actual, exp) in _zip_dicts(audio_trascriptions, expected)}
        resultManager.save(case, result)


def analyze(args):
    final_result = defaultdict(list)
    for case in _cases():
        tags = tagManager.load_code(case)
        final_result[tags].append(resultManager.load(case))

    _save_to_csv(final_result)



config = toml.load('config.toml')
tagManager = TagManager(config['Tags'])
expectedManager = ExpectedManager()
resultManager = ResultManager()

#
#def repair_expected(loc : Path, create=False):
#    expected_path = loc.joinpath('expected.txt')
#    expected_path.touch(exist_ok=True)
#
#    data = expectedManager.load(expected_path)
#    audio_files = _get_audio_files(loc).keys()
#    data = { x:'' for x in audio_files } | data
#
#    expectedManager.save(expected_path, data)