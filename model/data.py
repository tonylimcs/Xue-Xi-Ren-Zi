from engine.processor import remove_english, process, tokenize
from engine.filter import filter_pos

from model.io import get_article, get_user_db
from model.text_formatter import init_format


class Data:

    def __init__(self):
        self.tokens, py_list = [], []
        lines = get_article('articles/1.txt')
        for count, line in enumerate(lines):
            print(f'{count + 1} of {len(lines)}')
            line = line.strip('\n')
            line, eng_words = remove_english(line)
            py_full, py_only, chars_only = process(line)
            py_list += py_only
            self.tokens += tokenize(py_full, chars_only, eng_words)
            self.tokens += '<br><br>'

        self.user = get_user_db('database/user.json')
        unseen_pos, self.learning_pos = filter_pos(self.user, self.tokens, py_list)
        # Update user_db.json file
        self.text = init_format(self.tokens, learning=self.learning_pos, unseen=unseen_pos)


data = Data()
