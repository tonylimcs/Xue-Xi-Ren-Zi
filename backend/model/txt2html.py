from gui.font import color
from backend.engine.utils import num2dia
from backend.engine.constants import keys


def __wrap_highlight_html(text: str, color_: str) -> str:
    return f'<span style="background-color: {color_}">{text}</span>'


def highlight_hanzi(hanzi: str) -> str:
    return __wrap_highlight_html(hanzi, color.YELLOW)


def __wrap_size_html(text: str, size: int) -> str:
    """
    Wrap text with HTML format of the font tag for size.
    :param text: string to be embedded
    :param size: size of the text
    :return: HTML format of the string with the font size tag
    """
    return f"<font size={size}>{text}</font>"


def show_pinyin(hanzi: str, pinyin: str) -> str:
    """
    Show pinyin beside the hanzi.
    :param hanzi: Chinese character
    :param pinyin: pinyin of the character
    :return: string of the character with its pinyin beside
    """
    tagged_pinyin = __wrap_size_html(f"[{num2dia(pinyin)}]", 2)
    return f'{hanzi}{tagged_pinyin}'


def __wrap_color_html(text: str, color_: str) -> str:
    """
    Wrap text with HTML format of the font tag for color.
    :param text: string to be wrapped with HTML tags
    :param color_: color of the text
    :return: HTML format of the string with the font color tag
    """
    return f"<font color='{color_}'>{text}</font>"


_COLOR_CODE = {
    keys.LEARNED: color.GRAY,
    keys.LEARNING: color.ORANGE,
    keys.UNSEEN: color.BLACK,
    keys.WRONG: color.RED,
    keys.CORRECT: color.GREEN,
}


def color_code(text: str, status: str) -> str:
    """
    Color code the text corresponding to the status.
    :param text: the string to be color coded
    :param status: 'learned'/'learning'/'unseen'/'wrong'/'correct'
    :return: HTML format of the string with the font color tag
    corresponding to the status
    """
    return __wrap_color_html(text, color_=_COLOR_CODE[status])
