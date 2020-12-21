from bs4 import BeautifulSoup


def import_data(filename):
    """
    Purpose: Import data

    :param filename: str. Full path to MHTML

    :return content:
    """

    with open(filename, 'r') as f:
        content = f.read()
    f.close()

    return content


def soup_it(content):

    page_content = BeautifulSoup(content, "html.parser")

    return page_content
