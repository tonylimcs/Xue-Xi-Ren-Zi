from backend.engine.processor import remove_english, process, tokenize
from backend.engine.filter import filter_pos

from backend.model.io import get_article, get_user_db, update_user_db
from backend.model.text_formatter import init_format

from backend.keys import *

_USER_JSON = 'database/user.json'


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Data(metaclass=SingletonMeta):
    def __init__(self):
        self.tokens, py_list = [], []
        lines = get_article('articles/test.txt')
        print("processing...")
        for count, line in enumerate(lines):
            print(f'{count + 1} of {len(lines)} lines')
            line, eng_words = remove_english(line)
            py_full, py_only, chars_only = process(line)
            py_list += py_only
            self.tokens += tokenize(py_full, chars_only, eng_words)
            self.tokens += ["<br><br>"]
        self.tokens.pop()   # No need to break line for the last line

        self.user = get_user_db(_USER_JSON)
        unseen_pos, self.learning_pos = filter_pos(self.user, self.tokens, py_list)
        update_user_db(_USER_JSON, self.user)
        self.text = init_format(self.tokens, learning=self.learning_pos, unseen=unseen_pos)

    def update_counter(self, char, pinyin, is_correct):
        if is_correct:
            self.user[LEARNING][char][pinyin] -= 1
            counter = self.user[LEARNING][char][pinyin]
            print(f"**Correct!\n{char}({pinyin}): {counter}**")

            if counter == 0:
                self.update_learned(char, pinyin)
        else:
            self.user[LEARNING][char][pinyin] = self.user[REPETITION]  # Reset counter
            counter = self.user[LEARNING][char][pinyin]
            print(f"**Wrong. Reset counter.\n{char}[{pinyin}]: {counter}**")

    def get_counter(self, char, pinyin):
        if char in self.user[LEARNING] \
                and pinyin in self.user[LEARNING][char]:
            return self.user[LEARNING][char][pinyin]

        return 0

    def update_learned(self, char, pinyin):
        if char not in self.user[LEARNED]:
            # Initialize
            self.user[LEARNED][char] = []

        if pinyin not in self.user[LEARNED][char]:  # Avoid duplication
            self.user[LEARNED][char].append(pinyin)

        # Remove from "learning"
        del self.user[LEARNING][char][pinyin]
        if len(self.user[LEARNING][char]) == 0:
            del self.user[LEARNING][char]

    def update_json(self):
        update_user_db(_USER_JSON, self.user)

    def find_state(self, char, pinyin):
        state = UNSEEN
        for s in [LEARNED, LEARNING]:
            if char in self.user[s] \
                    and pinyin in self.user[s][char]:
                state = s
                break
        return state


data = Data()
