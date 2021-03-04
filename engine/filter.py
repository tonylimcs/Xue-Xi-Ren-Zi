from engine.utils import is_chinese


def update_learning(char, pinyin, learning, repeat):
    if char not in learning:
        # Initialize
        learning[char] = {}

    learning[char][pinyin] = repeat


def filter_pos(user_db, tokens, py_list):
    """
    Filter unseen and learning Chinese characters, and get their positions in the text
    :param user_db: user database
    :param tokens: tokenized text
    :param py_list: list of pinyin of its respective character in the text
    :return: lists of positions of unseen chars and learning chars respectively
    """
    repeat = user_db["repeat"]
    learned, learning = user_db["learned"], user_db["learning"]
    unseen_pos, learning_pos = [], []
    idx = 0
    for pos, token in enumerate(tokens):
        if is_chinese(token):
            pinyin = py_list[idx]
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
                update_learning(token, pinyin, learning, repeat)

    return unseen_pos, learning_pos
