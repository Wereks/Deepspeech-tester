import wave
import numpy as np
import deepspeech

MODEL_NAME = "deepspeech-0.9.2-models.pbmm"
SCORER_NAME = "deepspeech-0.9.2-models.scorer"
MODEL = None


def transcript(path):
    global MODEL
    if not MODEL:
        MODEL = deepspeech.Model(MODEL_NAME)
        MODEL.enableExternalScorer(SCORER_NAME)


    with wave.open(str(path), 'rb') as fin:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    return MODEL.stt(audio)