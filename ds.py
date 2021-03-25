import wave
import numpy as np
import deepspeech

MODEL = deepspeech.Model("deepspeech-0.9.2-models.pbmm")
MODEL.enableExternalScorer("deepspeech-0.9.2-models.scorer")


def transcript(path):
    with wave.open(str(path), 'rb') as fin:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    return MODEL.stt(audio)