import re

chinese = re.compile(u'[\u4e00-\u9fff]')


def is_chinese(word: str) -> bool:
    """
    Check if the word is Chinese
    """
    return True if chinese.search(word) else False
