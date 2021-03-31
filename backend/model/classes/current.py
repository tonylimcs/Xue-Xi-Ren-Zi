from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character
from backend.engine.constants import keys

from backend.model.classes.parsed import Parsed


class Current(metaclass=SingletonMeta):
    def __init__(self):
        self._parsed = Parsed()
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
        @return: tuple(index of phrase/char, index of char in phrase)
        """
        if idx:
            parsed = self._parsed.parsed
            p, s0, s1 = idx
            for i in range(p, len(parsed)):
                for j in range(s0, len(parsed[i])):
                    entity = parsed[i][j]
                    if isinstance(entity, ZHEntity):
                        chars = []
                        if isinstance(entity, Phrase):
                            chars += entity.chars
                        elif isinstance(entity, Character):
                            chars.append(entity)

                        for k in range(s1, len(chars)):
                            if chars[k].status == keys.LEARNING \
                                    and (i, j, k) not in self._parsed.unseen:
                                return i, j, k
                        s1 = 0  # Reset
                    s0 = 0  # Reset
        return tuple()

    def __init_idx(self) -> [tuple, None]:
        """
        Initialize the current index.
        @return: tuple(line #, pos in line, pos in phrase)
        """
        return self.__get_idx((0, 0, 0))

    def __update_idx(self) -> None:
        """
        Update current index from the parsed list to the next index
        for subsequent search.
        """
        parsed = self._parsed.parsed
        zh_entity = parsed[self._idx[0]][self._idx[1]]
        is_next_valid = True
        if isinstance(zh_entity, Phrase):
            self._idx = (self._idx[0],
                         self._idx[1],
                         self._idx[2] + 1)  # Update to next hanzi in phrase

            is_next_valid = self._idx[2] < len(zh_entity)   # Validate next hanzi in phrase

        if isinstance(zh_entity, Character) or not is_next_valid:
            self._idx = (self._idx[0],
                         self._idx[1] + 1,  # Update to next pos in line
                         0)     # Reset

        if self._idx[1] >= len(parsed[self._idx[0]]):
            # Has exceeded the line
            self._idx = (self._idx[0] + 1,  # Update to next line
                         0, 0)  # Reset

        self._idx = self.__get_idx(self._idx)

    def __get_cur(self) \
            -> [(Phrase, Character), (None, Character), (None, None)]:
        cur_phrase, cur_char = None, None
        if self._idx:
            parsed = self._parsed.parsed
            zh_entity = parsed[self._idx[0]][self._idx[1]]
            if isinstance(zh_entity, Phrase):
                cur_phrase = zh_entity
                cur_char = zh_entity.chars[self._idx[2]]
            elif isinstance(zh_entity, Character):
                cur_char = zh_entity
        return cur_phrase, cur_char

    def update_cur(self) -> None:
        self.__update_idx()
        self._phrase, self._char = self.__get_cur()

    def update(self):
        self.__init__()
