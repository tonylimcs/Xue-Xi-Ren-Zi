from backend.model.classes.parsed import Parsed
from backend.model.classes.body import Body
from backend.model.classes.current import Current

from file_paths import ARTICLE_PATH

"""
ARTICLE_PATH is just a placeholder;
may get input dynamically from a recommender in the future.
"""
p = Parsed(ARTICLE_PATH)
p.subscribe(Body(), Current())

