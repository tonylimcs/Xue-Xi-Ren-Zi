from engine.utils import is_chinese


def update_learning(char, pinyin, learning):
    if char not in learning:
        # initialize
        learning[char] = [pinyin]
    else:
        learning[char].append(pinyin)


def filter_pos(user_db, tokens, py_list):
    """
    Filter unseen and learning Chinese characters, and get their positions in the text
    :param user_db: user database
    :param tokens: tokenized text
    :param py_list: list of pinyin of its respective character in the text
    :return: lists of positions of unseen chars and learning chars respectively
    """
    learned, learning = user_db["learned"], user_db["learning"]
    unseen_pos, learning_pos = [], []
    idx = 0
    for pos, token in enumerate(tokens):
        if is_chinese(token):
            pinyin = py_list[idx]
            idx += 1
            if token in learned and pinyin in learned[token]:
                continue

            if token in learning:
                if pinyin in learning[token]:
                    learning_pos.append((pos, pinyin))
                else:
                    unseen_pos.append((pos, pinyin))
                    update_learning(token, pinyin, learning)
            else:
                unseen_pos.append((pos, pinyin))
                update_learning(token, pinyin, learning)

    return unseen_pos, learning_pos
