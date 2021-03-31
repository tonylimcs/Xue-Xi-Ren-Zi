from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character

from backend.model.classes.parsed import Parsed
from backend.model.txt2html import *


class Body(metaclass=SingletonMeta):
    def __init__(self):
        self._parsed = Parsed()
        self._body_html = self.__init_body_html()

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @property
    def body_html(self):
        return self._body_html

    def __init_body_html(self) -> str:
        """
        Convert parsed lines into a string of HTML format
        for the body text to be displayed on the GUI.
        @return: a string of HTML format
        """
        html_str = ''
        is_first = True
        unseen_idx = self._parsed.unseen
        for i, parsed_line in enumerate(self._parsed.parsed):
            line = ''
            for j, e in enumerate(parsed_line):
                token = e
                if isinstance(e, ZHEntity):
                    chars = []
                    if isinstance(e, Phrase):
                        chars += e.chars
                    if isinstance(e, Character):
                        chars.append(e)

                    hanzi_str = ''
                    for k, ch in enumerate(chars):
                        wrapped_str = ch.hanzi
                        idx = (i, j, k)
                        if idx in unseen_idx:
                            # Show pinyin for 'unseen' hanzi
                            wrapped_str = show_pinyin(ch.hanzi, ch.pinyin)
                            wrapped_str = color_code(wrapped_str, status=keys.UNSEEN)
                        elif ch.status == keys.LEARNING:
                            if is_first:
                                # Highlight the first 'learning' hanzi
                                wrapped_str = highlight_hanzi(ch.hanzi)
                                is_first = False    # Update flag
                            wrapped_str = color_code(wrapped_str, status=keys.LEARNING)
                        else:
                            # Color for 'learned' hanzi is already the default
                            pass

                        hanzi_str += wrapped_str
                    token = hanzi_str
                line += token

            if line:
                html_str += f'<p>{line}</p>'  # Each line is a paragraph
        return html_str

    def update_highlight(self, char: Character) -> None:
        if char is None:
            return

        original = color_code(char.hanzi, status=keys.LEARNING)

        highlighted_hanzi = highlight_hanzi(char.hanzi)
        updated = color_code(highlighted_hanzi, status=keys.LEARNING)

        self._body_html = self.body_html.replace(original, updated, 1)

    def update_answer(self, hanzi: str, pinyin: str, correct: bool) -> None:
        original = highlight_hanzi(hanzi)
        original = color_code(original, status=keys.LEARNING)

        updated = hanzi
        if not correct:
            updated = show_pinyin(hanzi, pinyin)
        result = keys.CORRECT if correct else keys.WRONG
        updated = color_code(updated, status=result)

        self._body_html = self.body_html.replace(original, updated, 1)

    def update_to_learned(self, hanzi: str) -> None:
        original = color_code(hanzi, status=keys.LEARNING)
        self._body_html = self.body_html.replace(original, hanzi)

    def update(self):
        self.__init__()
