from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character
from backend.engine.parser import parse
from backend.engine.io import get_article
from backend.engine.constants import keys


class _ParsedSingletonMeta(type):
    _instance = None
    _article_path = None

    def __call__(cls, article_path: str = ''):
        if article_path:
            if cls._instance is None:
                instance = super().__call__(article_path)
                cls._instance = instance
                cls._article_path = article_path
            else:
                assert cls._article_path == article_path, \
                    "Please use the instance method for update, " \
                    "e.g. Parsed().update(article_path)."
        else:
            assert cls._instance is not None, \
                "Initialize by giving a path to the article as an argument first!"
        return cls._instance


class Parsed(metaclass=_ParsedSingletonMeta):
    _listeners = []

    def __init__(self, article_path: str = ''):
        self._article_path = article_path
        self._parsed = self.__init_parsed()
        self._unseen = self.__init_unseen()

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"(listeners: {self._listeners})"

    @property
    def article_path(self):
        return self._article_path

    @property
    def parsed(self):
        return self._parsed

    @property
    def unseen(self):
        return self._unseen

    def __init_parsed(self) -> list:
        lines = get_article(self.article_path)
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

    def subscribe(self, *listeners) -> None:
        for listener in listeners:
            print(f"(Publisher) {self.__class__.__name__}: "
                  f"Subscribing...{listener.__class__.__name__}")
            self._listeners.append(listener)

    def unsubscribe(self, *listeners) -> None:
        for listener in listeners:
            print(f"(Publisher) {self.__class__.__name__}: "
                  f"Unsubscribing...{listener.__class__.__name__}")
            self._listeners.remove(listener)

    def notify(self) -> None:
        for listener in self._listeners:
            print(f"(Publisher) {self.__class__.__name__}: "
                  f"Notifying...{listener.__class__.__name__}")
            listener.update()

    def update(self, article_path: str):
        self.__init__(article_path)
        self.notify()
