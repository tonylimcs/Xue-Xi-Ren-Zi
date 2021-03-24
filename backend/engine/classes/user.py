from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.io import get_user_db, save_user_db
from backend.engine.constants.keys import *

from file_paths import USER_DB_PATH

_INIT_USER_DB = {LEARNED: {}, LEARNING: {},
                 ARTICLES: [],
                 REPETITION: 5}     # Value may be modified to suit user's preference


class User(metaclass=SingletonMeta):
    def __init__(self):
        self._user = self.__init_user()

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"({LEARNED}: {len(self._user[LEARNED])}, " \
               f"{LEARNING}: {len(self._user[LEARNING])}, " \
               f"{ARTICLES}: {self._user[ARTICLES]}, " \
               f"{REPETITION}: {self._user[REPETITION]})"

    @staticmethod
    def __init_user() -> dict:
        user_ = get_user_db(USER_DB_PATH)
        if user_ is None:
            user_ = _INIT_USER_DB
        return user_

    def __update_learned(self, hanzi: str, pinyin: str) -> None:
        if hanzi not in self._user[LEARNED]:
            # Initialize
            self._user[LEARNED][hanzi] = []

        if pinyin not in self._user[LEARNED][hanzi]:  # Prevent duplication
            print(f"[USER] New character learned: {hanzi}!")
            self._user[LEARNED][hanzi].append(pinyin)

        if self.is_status(hanzi, pinyin, status=LEARNING):
            # Remove from 'learning'
            del self._user[LEARNING][hanzi][pinyin]
            if len(self._user[LEARNING][hanzi]) == 0:
                del self._user[LEARNING][hanzi]

    def __update_learning(self, hanzi: str, pinyin: str) -> None:
        if hanzi not in self._user[LEARNING]:
            # Initialize
            self._user[LEARNING][hanzi] = {}

        if pinyin not in self._user[LEARNING][hanzi]:
            self._user[LEARNING][hanzi][pinyin] = self._user[REPETITION]

    def update_status(self, hanzi: str, pinyin: str, status: str) -> None:
        if status == LEARNED:
            self.__update_learned(hanzi, pinyin)
        elif status == LEARNING:
            self.__update_learning(hanzi, pinyin)

    def get_counter(self, hanzi: str, pinyin: str) -> int:
        counter = -1
        if self.is_status(hanzi, pinyin, status=LEARNING):
            counter = self._user[LEARNING][hanzi][pinyin]
        elif self.is_status(hanzi, pinyin, status=LEARNED):
            counter = 0
        return counter

    def update_counter(self, hanzi: str, pinyin: str, correct: bool) -> None:
        if correct:
            self._user[LEARNING][hanzi][pinyin] -= 1
            result = 'Correct'
        else:
            self._user[LEARNING][hanzi][pinyin] = \
                self._user[REPETITION]  # Reset counter
            result = 'Wrong'

        counter = self._user[LEARNING][hanzi][pinyin]
        print(f"* {result}. {hanzi}[{pinyin}]: {counter} *")

    def update_articles(self, article_path) -> None:
        """
        Increment no. of articles read by the user.
        """
        if article_path not in self._user[ARTICLES]:    # Prevent duplication
            self._user[ARTICLES].append(article_path)

    def change_rep(self, repetition: int) -> None:
        """
        Change the number of times the user must input the pinyin
        of the same character correctly before considered as 'learned'.
        :param repetition: the number of times the user
        must repeatedly input the pinyin correctly for a given character
        """
        self._user[REPETITION] = repetition

    def get_status(self, hanzi: str, pinyin: str) -> str:
        status = UNSEEN
        for s in [LEARNED, LEARNING]:
            if self.is_status(hanzi, pinyin, status=s):
                status = s
                break
        return status

    def is_status(self, hanzi: str, pinyin: str, status: str) -> bool:
        return hanzi in self._user[status] \
               and pinyin in self._user[status][hanzi]

    def save_user(self) -> None:
        save_user_db(USER_DB_PATH, self._user)
