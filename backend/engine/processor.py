import re
from g2pc import G2pC
from backend.engine.utils import is_chinese, split_chinese

english = re.compile(u'[A-Za-z]+( [A-Za-z]+)*')

g2p = G2pC()


def remove_english(string: str):
    eng_data = []
    eng_all = english.finditer(string)
    eng_words = set()
    for eng in eng_all:
        eng_word = eng.group(0)
        eng_words.add(eng_word)
        eng_data.append((eng.start(), eng_word))

    for eng_word in eng_words:
        string = string.replace(eng_word, '')

    return string, eng_data


def process(text: str):
    data = g2p(text)
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
