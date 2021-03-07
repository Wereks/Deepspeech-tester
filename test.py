from utils import *
from pathlib import Path

import toml

def setup(dir : Path, code, tags):
    expected(dir, create=True)
    

    #Stworz expected
    #Stworz pliki db
    #Stworz tagi


def get_audio_files(loc : Path):
    audio_path = loc.joinpath('audio')
    audio_files = [x for x in audio_path.glob('*.wav') if x.is_file()]

    return audio_files

def expected(loc : Path, create=False):
    expected_path = loc.joinpath('expected.txt')
    expected_path.touch(exist_ok=True)

    data = load_expected_values(expected_path)
    audio_files = get_audio_files(loc)
    data = { x:'-' for x in audio_files } | data

    save_expected_values(expected_path, data)

def tags(loc : Path, code : str):
    #TODO
    tags_path = loc.joinpath('tags.txt')
    tags_path.touch(exist_ok=True)

    data = load_tags_values(expected_path)
    audio_files = get_audio_files(loc)
    data = { x:'-' for x in audio_files } | data

    save_expected_values(expected_path, data)

