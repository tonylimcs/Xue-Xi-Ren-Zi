from gui.font import color
from backend.engine.utils import num2dia

LEARNING = 'learning'
UNSEEN = 'unseen'
WRONG = 'wrong'
CORRECT = 'correct'


def tag_color_html(char: str, color_: str) -> str:
    """
    Embed text with HTML format of the font tag for color
    :param char: string to be embedded
    :param color_: color of the text
    :return: HTML format of the string with the font tag
    """
    return f"<font color='{color_}'>{char}</font>"


def tag_highlight_html(char: str, color_=color.YELLOW) -> str:
    return f'<span style="background-color: {color_}">{char}</span>'


def tag_size_html(char: str, size: int) -> str:
    """
    Embed text with HTML format of the font tag for size
    :param char: string to be embedded
    :param size: size of the text
    :return: HTML format of the string with the font tag
    """
    return f"<font size={size}>{char}</font>"


def format_color(char: str, tag: str = "") -> str:
    """
    Color code the text based on the tag
    :param char: Chinese character that the user is learning
    :param tag: learning/wrong/unseen
    :return: HTML format of the string with the font tag
    """
    if tag == LEARNING:
        color_ = color.ORANGE
    elif tag == WRONG:
        color_ = color.RED
    elif tag == CORRECT:
        color_ = color.GREEN
    elif tag == UNSEEN:
        color_ = color.BLACK
    else:
        color_ = color.GRAY

    return tag_color_html(char, color_)


def tag_pinyin(char: str, pinyin: str) -> str:
    """
    Tag pinyin beside the character
    :param char: Chinese character
    :param pinyin: pinyin of the character
    :return: string of the character with its pinyin beside
    """
    tagged = tag_size_html(f"[{num2dia(pinyin)}]", 2)
    return f'{char}{tagged}'


def init_format(tokens: list, unseen: list, learning: list) -> str:
    idx = {UNSEEN: 0, LEARNING: 0}
    new_str = ''
    for i, token in enumerate(tokens):
        cur = ''
        u_idx, l_idx = idx[UNSEEN], idx[LEARNING]
        if u_idx < len(unseen) and i == unseen[u_idx][0]:
            cur = UNSEEN
        elif l_idx < len(learning) and i == learning[l_idx][0]:
            cur = LEARNING

        if cur:
            if cur == UNSEEN:
                # show pinyin for "unseen" chars
                unseen_char = unseen[u_idx][1]
                token = tag_pinyin(token, unseen_char)
            elif cur == LEARNING and l_idx == 0:
                # highlight the first "learning" char
                token = tag_highlight_html(token)

            token = format_color(token, tag=cur)
            idx[cur] += 1   # update respective index

        new_str += token

    return new_str


def update_highlight(text: str, char: str) -> str:
    if char is None:
        return text

    old_char = format_color(char, tag=LEARNING)

    highlighted_char = tag_highlight_html(char)
    new_char = format_color(highlighted_char, tag=LEARNING)

    return text.replace(old_char, new_char, 1)


def update_format(text: str, cur_char: str, cur_pinyin: str, correct: bool) -> str:
    old_char = tag_highlight_html(cur_char)
    old_char = format_color(old_char, tag=LEARNING)

    result = CORRECT if correct else WRONG
    if not correct:
        cur_char = tag_pinyin(cur_char, cur_pinyin)

    new_char = format_color(cur_char, tag=result)

    return text.replace(old_char, new_char, 1)


def update_domino_effect(text: str, cur_char: str, counter: int):
    old_char = format_color(cur_char, tag=LEARNING)
    if counter == 0:
        return text.replace(old_char, cur_char)

    return text
