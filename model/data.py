from engine.processor import remove_english, process, tokenize
from engine.filter import filter_pos

from model.io import get_article, get_user_db, update_user_db
from model.text_formatter import init_format

USER_JSON = 'database/user.json'


class Data:

    def __init__(self):
        self.tokens, py_list = [], []
        lines = get_article('articles/test.txt')
        for count, line in enumerate(lines):
            print(f'{count + 1} of {len(lines)}')
            line, eng_words = remove_english(line)
            py_full, py_only, chars_only = process(line)
            py_list += py_only
            self.tokens += tokenize(py_full, chars_only, eng_words)
            self.tokens += ["<br><br>"]
        self.tokens.pop()   # No need to break line for the last line

        self.user = get_user_db(USER_JSON)
        unseen_pos, self.learning_pos = filter_pos(self.user, self.tokens, py_list)
        update_user_db(USER_JSON, self.user)
        self.text = init_format(self.tokens, learning=self.learning_pos, unseen=unseen_pos)

    def update_counter(self, char, pinyin, is_correct):
        if is_correct:
            self.user["learning"][char][pinyin] -= 1
            counter = self.user["learning"][char][pinyin]
            print(f"**Correct!\n{char}({pinyin}): {counter}**")

            if counter == 0:
                self.update_learned(char, pinyin)
        else:
            self.user["learning"][char][pinyin] = self.user["repeat"]  # Reset counter
            counter = self.user["learning"][char][pinyin]
            print(f"**Wrong. Reset counter.\n{char}[{pinyin}]: {counter}**")

    def update_learned(self, char, pinyin):
        if char not in self.user["learned"]:
            # Initialize
            self.user["learned"][char] = []

        if pinyin not in self.user["learned"][char]:
            # Avoid duplication
            self.user["learned"][char].append(pinyin)

        # Remove from "learning"
        del self.user["learning"][char][pinyin]
        if len(self.user["learning"][char]) == 0:
            del self.user["learning"][char]

    def update_json(self):
        update_user_db(USER_JSON, self.user)


data = Data()
