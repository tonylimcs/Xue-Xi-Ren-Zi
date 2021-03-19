from backend.engine.utils import is_chinese
from backend.keys import *


def update_learning(char, pinyin, learning, repeat):
    if char not in learning:
        # Initialize
        learning[char] = {}

    learning[char][pinyin] = repeat


def filter_pos(user_db, tokens, pinyin_ls):
    """
    Filter unseen and learning Chinese characters, and get their positions in the text
    :param user_db: user database
    :param tokens: tokenized text
    :param pinyin_ls: list of pinyin
    :return: lists of positions of unseen chars and learning chars respectively
    """
    repetition = user_db[REPETITION]
    learned, learning = user_db[LEARNED], user_db[LEARNING]
    unseen_pos, learning_pos = [], []
    idx = 0
    for pos, token in enumerate(tokens):
        if is_chinese(token):
            pinyin = pinyin_ls[idx]
            idx += 1
            if token in learned and pinyin in learned[token]:
                continue

            flag = True
            if token in learning:
                if pinyin in learning[token]:
                    learning_pos.append((pos, pinyin))
                    flag = False

            if flag:
                unseen_pos.append((pos, pinyin))
                update_learning(token, pinyin, learning, repetition)

    return unseen_pos, learning_pos
