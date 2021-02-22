import json


def get_article(file_path):
    """
    Get content of the article
    :param file_path: path of the article (.txt)
    :return: list of lines from the article
    """
    with open(file_path, "r", encoding='utf-8') as f:
        return f.readlines()


def get_user_db(file_path):
    """
    Get user database
    :param file_path: path of the user database (.json)
    :return: dictionary of user data
    """
    with open(file_path) as f:
        return json.load(f)


def update_user_db(file_path, user_db):
    """
    Update user database
    :param file_path: path of the user database (.json)
    :param user_db: dictionary of updated user data
    """
    with open(file_path, 'w') as f:
        json.dump(user_db, f)
