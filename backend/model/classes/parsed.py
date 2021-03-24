from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character
from backend.engine.parser import parse
from backend.engine.io import get_article
from backend.engine.constants import keys


_ARTICLE_PATH = 'articles/1.txt'


class _ParsedSingleton(metaclass=SingletonMeta):
    def __init__(self):
        self._parsed = self.__init_parsed()
        self._unseen = self.__init_unseen()

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"(unseen: {len(self.unseen)})"

    @property
    def parsed(self):
        return self._parsed

    @property
    def unseen(self):
        return self._unseen

    @staticmethod
    def __init_parsed() -> list:
        lines = get_article(_ARTICLE_PATH)
        return parse(lines)

    def __init_unseen(self) -> set:
        unseen_ = set()
        for i, e in enumerate(self.parsed):
            if isinstance(e, ZHEntity):
                chars = []
                if isinstance(e, Phrase):
                    chars += e.chars
                elif isinstance(e, Character):
                    chars.append(e)

                for j, ch in enumerate(chars):
                    idx = (i, j)
                    if ch.status == keys.UNSEEN \
                            and idx not in unseen_:
                        unseen_.add(idx)
                        ch.status = keys.LEARNING   # Update status
        return unseen_


class Parsed:
    _parsed = _ParsedSingleton()

    def __new__(cls, *args, **kwargs):
        return _ParsedSingleton()

    def __repr__(self):
        return repr(self._parsed)
