from constants import diacritical as dia
import re
from utils import is_chinese, split_chinese

english = re.compile(u'[A-Za-z]+( [A-Za-z]+)*')


def preprocess(string: str, eng_data: list):
    eng_all = english.finditer(string)
    eng_words = set()
    for eng in eng_all:
        eng_word = eng.group(0)
        eng_words.add(eng_word)
        eng_data.append((eng.start(), eng_word))

    for eng_word in eng_words:
        string = string.replace(eng_word, '')

    return string, eng_data


def process(data: list):
    pinyin_full, pinyin_only, chars_only = [], [], []
    for tup in data:
        try:
            if is_chinese(tup[0]):
                tup_split = tup[2].split()
                pinyin_only += [char for char in tup_split]     # flatten the list
                pinyin_full.append(tuple(tup_split))            # pinyin indicated by tuple
                chars_only += split_chinese(tup[0])
            else:
                pinyin_full.append(tup[0])
        except IndexError:
            continue

    return pinyin_full, pinyin_only, chars_only


def tokenize(pinyin_full: list, chars_only: list, eng_data: list) -> list:
    tokens = []
    pos = 0
    idx = 0
    for i, obj in enumerate(pinyin_full):
        try:
            is_english = eng_data[0][0] == pos
        except IndexError:
            is_english = False
        is_pinyin = type(obj) is tuple

        if is_english:
            # append removed English words
            eng = eng_data.pop(0)
            eng_word = eng[1]
            tokens.append(eng_word)
            pos += len(eng_word)

        if is_pinyin:
            # append Chinese characters
            for j in range(len(obj)):
                tokens.append(chars_only[idx])
                pos += 1
                idx += 1
        else:
            # append numbers or punctuations
            pos += 1
            tokens.append(obj)

    return tokens


def num2dia(pinyin: str) -> str:
    """
    Convert tone representation: numerical -> diacritical
    :param pinyin: pinyin of a Chinese character
    :return: diacritical format of the pinyin
    """
    if len(pinyin) > 1 and re.match(r"\d{1.txt,5}", pinyin[-1]):
        tone = int(pinyin[-1])
        if tone == 5:
            # neutral tone
            return pinyin[:-1]

        try:
            # special case
            pos = re.search('(?<=i)u', pinyin).start()
            return pinyin[:pos] + dia[tone - 1][4] + pinyin[pos + 1:-1]
        except AttributeError:
            pass

        for i, v in enumerate(['a', 'e', 'i', 'o', 'u']):
            try:
                pos = re.search(v, pinyin).start()
                return pinyin[:pos] + dia[tone - 1][i] + pinyin[pos + 1:-1]
            except AttributeError:
                continue

    return pinyin
