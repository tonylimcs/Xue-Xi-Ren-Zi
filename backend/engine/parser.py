from backend.engine import g2p
from backend.engine.classes.zh_entity import create_zh_entity

import re

english = re.compile(u'[A-Za-z]+( [A-Za-z]+)*')


def get_en_phrases(line: str) -> list:
    """
    Get English phrases, if any, from the given string.
    The order of the positions is to be preserved.
    :param line: the text that English phrases (if any) are to be extracted from
    :return: a list of English phrases
    """
    en_all = english.finditer(line)
    return [en.group(0) for en in en_all]


def remove_en_phrases(line: str, en_phrases: list) -> str:
    """
    Remove English phrases, if any, from the given string.
    :param line: a line from the article
    :param en_phrases: a list of English phrases
    :return: the string without any English phrases
    """
    unique_phrases = set(en_phrase for en_phrase in en_phrases)     # Prevent overhead from repeated search
    for en_phrase in unique_phrases:
        line = line.replace(en_phrase, '|')    # Placeholder to represent existed English phrase
    return line


def restore_en_phrases(parsed: list, en_phrases: list) -> list:
    """
    Restore removed English phrases, if any.
    :param parsed: the parsed list
    :param en_phrases: the list of English phrases that were removed
    :return: the parsed list with the English phrases restored
    """
    if len(en_phrases) == 0:
        return parsed

    restored = []
    for e in parsed:
        if e == '|':
            restored.append(en_phrases.pop(0))
        else:
            restored.append(e)
    return restored


def parse_line(line: str) -> list:
    parsed_line = []
    parsed = g2p(line)
    for tup in parsed:
        entity = create_zh_entity(tup[0], tup[2], tup[4])
        if entity is None:
            entity = tup[0]
        parsed_line.append(entity)
    return parsed_line


def parse(lines: list) -> list:
    parsed = []
    print('\n*** Parsing Commenced ***')
    for count, line in enumerate(lines):
        print(f'parsing...{count + 1} of {len(lines)} lines')
        en_phrases = get_en_phrases(line)
        line = remove_en_phrases(line, en_phrases)
        parsed_line = parse_line(line)
        parsed += restore_en_phrases(parsed_line, en_phrases)
        parsed.append('\n\n')
    parsed.pop()    # Don't need new lines after the last line
    print('*** Parsing Finished ***\n')
    return parsed
