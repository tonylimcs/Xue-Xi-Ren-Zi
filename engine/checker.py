import re


def check_correct(user_input: str, learning: list, tokens: list):
    cur = learning.pop(0)
    cur_pos, cur_pinyin = cur[0], cur[1]
    cur_char = tokens[cur_pos]

    if not re.match(r'\d', user_input[-1]):
        user_input += '5'

    result = user_input == cur_pinyin
    return result, cur_char, cur_pinyin
