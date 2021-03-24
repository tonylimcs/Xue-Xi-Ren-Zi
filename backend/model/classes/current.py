from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character
from backend.engine.constants import keys

from backend.model.classes.parsed import Parsed


class Current(metaclass=SingletonMeta):
    _parsed = Parsed()

    def __init__(self):
        super(Current, self).__init__()

        self._idx = self.__init_idx()   # Current index from parsed list
        self._phrase, self._char = self.__get_cur()

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"(phrase: {self.phrase}, char: {self.char})"

    @property
    def phrase(self):
        return self._phrase

    @property
    def char(self):
        return self._char

    def __get_idx(self, idx: tuple) -> tuple:
        """
        Get the index from the parsed list to test the user of its correct pinyin.
        :return: tuple(index of phrase/char, index of char in phrase)
        """
        if idx:
            parsed = self._parsed.parsed
            s0, s1 = idx
            for i in range(s0, len(parsed)):
                if isinstance(parsed[i], ZHEntity):
                    chars = []
                    if isinstance(parsed[i], Phrase):
                        chars += parsed[i].chars
                    elif isinstance(parsed[i], Character):
                        chars.append(parsed[i])

                    for j in range(s1, len(chars)):
                        if chars[j].status == keys.LEARNING \
                                and (i, j) not in self._parsed.unseen:
                            return i, j
                    s1 = 0  # Reset
        return tuple()

    def __init_idx(self) -> [tuple, None]:
        return self.__get_idx((0, 0))

    def __update_idx(self) -> None:
        """
        Update current index from the parsed list to the next index
        for subsequent search.
        """
        parsed = self._parsed.parsed
        zh_entity = parsed[self._idx[0]]
        if isinstance(zh_entity, Phrase):
            self._idx = (self._idx[0], self._idx[1] + 1)
            if self._idx[1] >= len(zh_entity):
                self._idx = (self._idx[0] + 1, 0)
        else:
            self._idx = (self._idx[0] + 1, 0)

        self._idx = self.__get_idx(self._idx)

    def __get_cur(self) \
            -> [(Phrase, Character), (None, Character), (None, None)]:
        cur_phrase, cur_char = None, None
        if self._idx:
            parsed = self._parsed.parsed
            zh_entity = parsed[self._idx[0]]
            if isinstance(zh_entity, Phrase):
                cur_phrase = parsed[self._idx[0]]
                cur_char = zh_entity.chars[self._idx[1]]
            elif isinstance(zh_entity, Character):
                cur_char = zh_entity
        return cur_phrase, cur_char

    def update_cur(self) -> None:
        self.__update_idx()
        self._phrase, self._char = self.__get_cur()
        print(self)
