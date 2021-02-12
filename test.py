from g2pc import G2pC
from constants import diacritical as dia
import re
from utils import is_chinese


test = "发出如此感慨的，是一位在中国生活了十年的美国小伙王德中（原名Cyrus Janssen）。"
test1 = "在《北京周报》（Beijing Review）推特账户9日发布的一段视频中，他讲述了自己从中国返美时的一段经历。而当时他的美国友人令人大跌眼镜的问题，把他给“整懵了”。"

# TODO: remove english text before processing; rejoin text after processing
def :


def get_pinyin(data: list):
    """
    Retrieve pinyin from data
    """
    pinyin_full, pinyin_only = [], []
    for tup in data:
        try:
            if is_chinese(tup[0]):
                tup_split = tup[2].split()
                pinyin_full.append(tuple(tup_split))
                pinyin_only += [char for char in tup_split]     # flatten the list
            else:
                pinyin_full.append(tup[0])
        except IndexError:
            continue

    return pinyin_full, pinyin_only


def num2dia(word: str) -> str:
    """
    Convert tone representation: numerical -> diacritical
    """
    if len(word) > 1 and re.match(r"\d{1,5}", word[-1]):
        tone = int(word[-1])

        if tone == 5:
            # neutral tone
            return word[:-1]

        for i, v in enumerate(['a', 'e', 'i', 'o', 'u']):
            try:
                pos = re.search(v, word).start()
                # replace numerical with diacritical
                return word[:pos] + dia[tone - 1][i] + word[pos + 1:-1]
            except AttributeError:
                continue

    return word


if __name__ == "__main__":
    g2p = G2pC()
    raw_data = g2p(test)
    print(raw_data)
    py_full, py_only = get_pinyin(raw_data)
    print(py_full)
    print(py_only)

    dia_py = [num2dia(py) for py in py_only]
    print(' '.join(dia_py))
