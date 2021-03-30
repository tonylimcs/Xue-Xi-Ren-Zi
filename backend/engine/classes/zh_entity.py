from backend.engine import g2p
from backend.engine.classes.user import User
from backend.engine.constants import keys
from backend.engine.utils import split_chinese, is_chinese

import re


class _ZHEntitySingletonMeta(type):
    _instances = {}

    def __call__(cls, hanzi: str, pinyin: str, meaning: str = ''):
        """
        A hanzi may have more than one pinyin,
        thus both hanzi and pinyin are required for uniqueness.
        """
        if (hanzi, pinyin) not in cls._instances:
            instance = super().__call__(hanzi, pinyin, meaning)
            cls._instances[(hanzi, pinyin)] = instance
        return cls._instances[(hanzi, pinyin)]


class ZHEntity(metaclass=_ZHEntitySingletonMeta):
    def __init__(self, hanzi: str, pinyin: str, meaning: str):
        """
        The 'entity' here refers to a Chinese character/phrase.
        :param hanzi: (汉字) the Chinese character
        :param pinyin: (拼音) the alphabet romanization
        :param meaning: the meaning of the entity
        """
        self._hanzi = hanzi
        self._pinyin = pinyin
        self.meaning = meaning

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"({self.hanzi}, {self.pinyin})"

    def __len__(self):
        """
        Length of Chinese word.
        Example, “你” = 1, "你好" = 2, "万事如意" = 4, ...
        :return: the number of Chinese characters
        """
        return len(self.hanzi)

    @property
    def hanzi(self):
        return self._hanzi

    @property
    def pinyin(self):
        return self._pinyin

    @property
    def meaning(self):
        return self._meaning

    @meaning.setter
    def meaning(self, value: str):
        self._meaning = re.sub(r'^/|/$', '', value)


class Character(ZHEntity):
    _user = User()

    def __init__(self, hanzi: str, pinyin: str, meaning: str = ''):
        """
        A Chinese character.
        The meaning can be automatically retrieved, if not already given.
        :param hanzi: (汉字) the Chinese character
        :param pinyin: (拼音) the alphabet romanization
        :param meaning: the meaning of the entity
        """
        super(Character, self).__init__(hanzi, pinyin, meaning)

        if not self.meaning:
            # Retrieve meaning
            self.meaning = g2p(self.hanzi)[0][4]

        # Retrieve status from user data
        self.status = self._user.get_status(hanzi, pinyin)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        assert value in [keys.LEARNED, keys.LEARNING, keys.UNSEEN], \
            "Status must be 'learned'|'learning'|'unseen'!"
        self._status = value

        # Update user data
        self._user.update_status(self.hanzi, self.pinyin,
                                 status=value)


class Phrase(ZHEntity):
    def __init__(self, hanzi: str, pinyin: str, meaning: str):
        """
        A phrase is a composition of more than one Chinese characters.
        Unlike Character objects, the meaning must be given,
        as to ensure that the phrase is indeed meaningful/exists in the dictionary.
        :param hanzi: (汉字) the string of Chinese characters
        :param pinyin: (拼音) the string of alphabet romanizations
        :param meaning: the meaning of the entity
        """
        super(Phrase, self).__init__(hanzi, pinyin, meaning)

        self._chars = self.__init_chars()

    def __init_chars(self) -> list:
        hanzi_ls = split_chinese(self.hanzi)
        pinyin_ls = self.pinyin.split()
        return [Character(hanzi, pinyin) for hanzi, pinyin in zip(hanzi_ls, pinyin_ls)]

    @property
    def chars(self):
        return self._chars


def create_zh_entity(hanzi: str, pinyin: str, meaning: str) \
        -> [Character, Phrase, None]:
    """
    Method for creating the appropriate object；
    returns None if entity is not Chinese.
    :param hanzi: (汉字) the Chinese character
    :param pinyin: (拼音) the alphabet romanization
    :param meaning: the meaning of the entity
    :return: the appropriate entity-type object
    """
    if is_chinese(hanzi):
        if len(hanzi) == 1:
            zh_entity = Character(hanzi, pinyin, meaning)
        else:
            zh_entity = Phrase(hanzi, pinyin, meaning)
        return zh_entity

    return None
