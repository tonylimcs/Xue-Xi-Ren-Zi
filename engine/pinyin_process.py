from constants import diacritical as dia
import re
from utils import is_chinese, split_chinese

english = re.compile(u'[A-Za-z]+( [A-Za-z]+)*')


def preprocess(string: str, eng_data: list):
    """
    Remove English words on the input string
    """
    eng_all = english.finditer(string)
    eng_words = set()
    for eng in eng_all:
        eng_word = eng.group(0)
        eng_words.add(eng_word)
        eng_data.append((eng.start(), eng_word))

    for eng_word in eng_words:
        string = string.replace(eng_word, '')

    return string, eng_data


def get_pinyin(data: list):
    """
    Retrieve pinyin from data
    """
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


def num2dia(word: str) -> str:
    """
    Convert tone representation: numerical -> diacritical
    """
    if len(word) > 1 and re.match(r"\d{1,5}", word[-1]):
        tone = int(word[-1])
        if tone == 5:
            # neutral tone
            return word[:-1]

        try:
            # special case
            pos = re.search('(?<=i)u', word).start()
            return word[:pos] + dia[tone - 1][4] + word[pos + 1:-1]
        except AttributeError:
            pass

        for i, v in enumerate(['a', 'e', 'i', 'o', 'u']):
            try:
                pos = re.search(v, word).start()
                return word[:pos] + dia[tone - 1][i] + word[pos + 1:-1]
            except AttributeError:
                continue

    return word


def tokenize(pinyin_full: list, chars_only: list, eng_data: list) -> list:
    """
    Concatenate all pinyin and rejoin English words according to the original string
    """
    tokens = []
    pos = 0
    char_id = 0
    for i, obj in enumerate(pinyin_full):
        try:
            is_english = eng_data[0][0] == pos
        except IndexError:
            is_english = False
        is_pinyin = type(obj) is tuple

        if is_english:
            # rejoin removed English words
            eng = eng_data.pop(0)
            eng_word = eng[1]

            tokens.append(eng_word)
            pos += len(eng_word)

        if is_pinyin:
            for j in range(len(obj)):
                tokens.append(chars_only[char_id])
                pos += 1
                char_id += 1
        else:
            # concatenate numbers or punctuations
            pos += 1
            tokens.append(obj)

    return tokens
