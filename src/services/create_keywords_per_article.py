from util.PostGreConnector import PostGreConnector
from nlp.TextBlobExtractor import TextBlobExtractor
import multiprocessing
import traceback
import json
from functools import reduce


def create_keywords_per_article():

    batch_size = 10000

    articles_count = get_articles_count()

    # Nifty trick from https://stackoverflow.com/a/17511341/2785479 to ceil a division
    batch_count = -(-articles_count // batch_size)

    for batch_num in range(batch_count):

        with PostGreConnector.from_configuration() as connector:

            start_index = batch_num * batch_size

            end_index = start_index + batch_size
            select_cursor = connector.create_cursor()

            select_cursor.execute("select id,content from articles order by id limit %s offset %s", (batch_size, start_index))
            rows = select_cursor.fetchall()

            try:
                print("Starting batch {0} to {1}".format(start_index, end_index))

                p = multiprocessing.Pool(5)
                inserts_to_do = p.map(process_articles, split_list(rows, 5))

                inserts_to_do = reduce(lambda prev, curr: prev + curr, inserts_to_do)

                insert_cursor = connector.create_cursor()

                inserted_values = ','.join(insert_cursor.mogrify("(%s,%s)", x).decode("utf-8") for x in inserts_to_do)
                insert_cursor.execute("insert into keywords_per_article(article_id, content_json) VALUES " + inserted_values)

                connector.commit()

                print("Commited batch {0} to {1}".format(start_index, end_index))
            except:
                print("Batch {0} to {1} failed.".format(start_index, end_index))

                # This prints the type, value, and stack trace of the
                # current exception being handled.
                traceback.print_exc()

                connector.rollback()
                raise


def get_articles_count():
    with PostGreConnector.from_configuration() as connector:
        count_cur = connector.create_cursor()

        count_cur.execute("select count(id) from articles")
        articles_count = count_cur.fetchone()[0]
    return articles_count


def split_list(array, wanted_parts=1):
    length = len(array)
    return [array[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def process_articles(rows):
    inserts_todo = []
    tb_extractor = TextBlobExtractor()

    for article in rows:
        article_id = article[0]
        content = article[1]

        noun_phrases = tb_extractor.extract_noun_phrases(content)
        np_json = json.dumps(noun_phrases)
        inserts_todo.append((str(article_id), np_json))

    return inserts_todo


if __name__ == "__main__":
    create_keywords_per_article()
