import os

from services.create_keywords_average import create_keywords_average
from services.import_articles import import_articles
from services.create_keywords_per_article import create_keywords_per_article
from util.Configuration import Configuration


def generate_all_data():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, Configuration()["data_path"])

    import_articles(filepath)
    create_keywords_per_article()
    create_keywords_average()


if __name__ == "__main__":
    generate_all_data()