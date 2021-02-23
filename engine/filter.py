def filter_pos(user_db, lut):
    """
    Filter unseen and learning Chinese characters, and get their positions in the text
    :param user_db: user database (.json)
    :param lut: look-up table for positions of Chinese characters
    :return: lists of positions of unseen chars and learning chars
    """
    learned, learning = user_db["learned"], user_db["learning"]
    unseen_pos, learning_pos = [], []
    for char in lut.keys():
        if char in learned:
            for pinyin in lut[char].keys():
                if pinyin not in learned[char]:
                    unseen_pos += lut[char][pinyin]
        elif char in learning:
            for pinyin in lut[char].keys():
                if pinyin in learning[char]:
                    learning_pos += lut[char][pinyin]
                else:
                    unseen_pos += lut[char][pinyin]
        else:
            for pos_list in lut[char].values():
                unseen_pos += pos_list

    return unseen_pos, learning_pos
