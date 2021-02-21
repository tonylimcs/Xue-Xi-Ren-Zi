def get_article(file_path):
    """
    Return a list of lines retrieved from text file
    """
    with open(file_path, "r", encoding='utf-8') as f:
        return f.readlines()
