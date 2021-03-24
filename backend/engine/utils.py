import re

# Diacritical format of tone representation
dia = [
    ['ā', 'ē', 'ī', 'ō', 'ū', 'ǖ'],
    ['á', 'é', 'í', 'ó', 'ú', 'ǘ'],
    ['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ'],
    ['à', 'è', 'ì', 'ò', 'ù', 'ǜ']
]

chinese = re.compile(u'[\u4e00-\u9fff]')


def is_chinese(word: str) -> bool:
    """
    Check if the word is Chinese
    :param word: a word/character
    :return: True if Chinese, else False
    """
    return True if chinese.search(word) else False


def split_chinese(string: str) -> list:
    """
    Split a string of Chinese phrase into characters
    :param string: Chinese phrase
    :return: list of Chinese characters
    """
    return chinese.findall(string)


def num2dia(pinyin: str) -> str:
    """
    Convert tone representation: numerical -> diacritical
    :param pinyin: pinyin of a Chinese character
    :return: diacritical format of the pinyin
    """
    has_tone = re.match(r"\d{1,5}", pinyin[-1])
    is_special = re.search('(?<=i)u', pinyin)
    if len(pinyin) > 1 and has_tone:
        tone = int(pinyin[-1])
        pinyin = pinyin[:-1]
        if tone == 5:
            # Neutral tone
            pass
        elif is_special:
            # Special case
            pinyin = pinyin.replace('u', dia[tone - 1][4])
        else:
            for i, vowel in enumerate(['a', 'e', 'i', 'o', 'u']):
                if vowel in pinyin:
                    pinyin = pinyin.replace(vowel, dia[tone - 1][i])
                    break
    return pinyin
