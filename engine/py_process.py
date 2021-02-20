from constants import diacritical as dia
import re
from utils import is_chinese

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
    pinyin_full, pinyin_only = [], []
    for tup in data:
        try:
            if is_chinese(tup[0]):
                tup_split = tup[2].split()
                pinyin_only += [char for char in tup_split]     # flatten the list
                pinyin_full.append(tuple(tup_split))            # pinyin indicated by tuple
            else:
                pinyin_full.append(tup[0])
        except IndexError:
            continue

    return pinyin_full, pinyin_only


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


def postprocess(pinyin_full: list, eng_data: list, numerical=False) -> str:
    """
    Concatenate all pinyin and rejoin English words according to the original string
    """
    new_str = ''
    pos = 0
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

            new_str += eng_word
            pos += len(eng_word)
            if is_pinyin:
                new_str += ' '

        if is_pinyin:
            # concatenate pinyin
            if not numerical:
                tmp = []
                for j, py in enumerate(obj):
                    tmp.append(num2dia(py))
                    pos += 1
                obj = tmp

            obj = ''.join(obj)
        else:
            # concatenate numbers or punctuations
            pos += 1

        new_str += obj

        # add whitespace between non-tuple pinyin or English words or numbers
        try:
            next_obj = pinyin_full[i + 1]
            next_is_pinyin = type(next_obj) is tuple
            next_is_number = re.match(r'\d', next_obj)
        except TypeError:
            next_is_number = False  # next object's data type is not a string
        except IndexError:
            next_is_pinyin, next_is_number = False, False   # end of list

        try:
            next_is_english = eng_data[0][0] == pos
        except IndexError:
            next_is_english = False

        if (is_pinyin or re.match(r'\d', obj)) and (next_is_pinyin or next_is_english):
            new_str += ' '
        elif is_pinyin and next_is_number:
            new_str += ' '

    return new_str
