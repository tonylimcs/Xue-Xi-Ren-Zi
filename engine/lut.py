from engine.utils import is_chinese


def get_lut(tokens, py_list):
    """
    Generate a look-up table for positions of Chinese characters in the text
    :param tokens: the tokenized text
    :param py_list: list that only contains pinyin of the text
    :return: {'character': {'pinyin': [positions], ...}, ...}
    """
    lut = {}
    idx = 0
    for i, token in enumerate(tokens):
        if is_chinese(token):
            pinyin = py_list[idx]
            if token not in lut:
                # initialise
                lut[token] = {}
                lut[token][pinyin] = []

            lut[token][pinyin].append(i)
            idx += 1

    return lut
