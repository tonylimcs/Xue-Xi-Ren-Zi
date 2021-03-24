import json


def get_article(file_path: str) -> [list, None]:
    """
    Get content of the article
    :param file_path: path of the article (.txt)
    :return: list of lines from the article
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            print(f"[I/O] Retrieving article...{file_path}")
            return f.readlines()
    except FileNotFoundError:
        print(f"[I/O] Article not found!...{file_path}")
        return None


def get_user_db(file_path: str) -> [dict, None]:
    """
    Get user database
    :param file_path: path of the user database (.json)
    :return: dictionary of user data
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            print(f"[I/O] Retrieving user data...{file_path}")
            return json.load(f)
    except FileNotFoundError:
        print(f"[I/O] No existing user data found.")
        return None


def save_user_db(file_path: str, user_db: dict) -> None:
    """
    Save user database to json file
    :param file_path: path of the user database (.json)
    :param user_db: dictionary of updated user data
    """
    with open(file_path, 'w') as f:
        print(f"[I/O] Saving user data...{file_path}")
        json.dump(user_db, f)
