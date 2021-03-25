from pathlib import Path

from pylev import levenshtein

from .iop import result


METRICS_ONE = {
    'text': lambda x, y: x,
    'expected': lambda x, y: y,
    'plt': levenshtein,
    'pwt': lambda x,y: levenshtein(x.split(), y.split()),
}



def _calculate(points, text, expected):
    return 1 - points / (len(text) + len(expected) + 1)

def _calculate_letters(dct: dict):
    sum_of_metrics = sum(_calculate(result['plt'], result['text'], result['expected']) for result in dct.values())
    sum_of_metrics = sum_of_metrics / len(dct)

    return "{:.2%}".format(sum_of_metrics)
    
def _calculate_words(dct: dict):
    sum_of_metrics = sum(_calculate(result['pwt'], result['text'].split(), result['expected'].split()) for result in dct.values())
    sum_of_metrics = sum_of_metrics / len(dct)

    return "{:.2%}".format(sum_of_metrics)


METRICS_WHOLE = {
    'plt': _calculate_letters,
    'pwt': _calculate_words
}



class ResultManager():

    def load(self, loc: Path) -> dict:
        return result.load(loc)

    def save(self, loc: Path, data):
        result.save(loc, data)

    def calculate(self, text : str, expected: str):
        text = text.lower()
        expected = expected.lower()
        result =  {name: metric(text, expected) for name, metric in METRICS_ONE.items()}

        return result

    def categories(self):
        return METRICS_WHOLE.keys()

    def calculate_whole(self, result: dict):
        result =  {name: metric(result) for name, metric in METRICS_WHOLE.items()}    
        return result