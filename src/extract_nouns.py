from util.PostGreConnector import PostGreConnector
from nlp.TextBlobExtractor import TextBlobExtractor
import multiprocessing
import traceback
import json
import time
from functools import reduce

select_query = "select id,content from articles order by id limit %s offset %s"


def main():

    batch_size = 10000

    with PostGreConnector.from_configuration() as connector:
        count_cur = connector.create_cursor()

        count_cur.execute("select count(id) from articles")
        articles_count = count_cur.fetchone()[0]

    # Nifty trick from https://stackoverflow.com/a/17511341/2785479 to ceil a division
    batch_count = -(-articles_count // batch_size)

    for batch_num in range(batch_count):
        with PostGreConnector.from_configuration() as connector:

            batch_start = (batch_num * batch_size)
            batch_end = batch_start + batch_size
            select_cur = connector.create_cursor()

            select_cur.execute(select_query, (batch_size, batch_start))
            rows = select_cur.fetchall()

            try:
                print("Starting batch {0} to {1}".format(batch_start, batch_end))

                extract_start = time.time()

                p = multiprocessing.Pool(5)
                inserts_to_do = p.map(process_batch, split_list(rows, 5))
                inserts_to_do = reduce(lambda x,y: x + y, inserts_to_do)

                extract_end = time.time()
                print("Extracting noun phrases took {0} seconds".format(str(extract_end - extract_start)))

                insert_cur = connector.create_cursor()

                insert_start = time.time()

                args_str = ','.join(insert_cur.mogrify("(%s,%s)", x).decode("utf-8") for x in inserts_to_do)
                insert_cur.execute("insert into nouns(article_id, content_json) VALUES" + args_str)

                connector.commit()

                insert_end = time.time()

                print("Inserting noun phrases took {0} seconds".format(str(insert_end - insert_start)))

                print("Commited batch {0} to {1}".format(batch_start, batch_end))
            except:
                print("Batch {0} to {1} failed.".format(batch_start, batch_end))

                # This prints the type, value, and stack trace of the
                # current exception being handled.
                traceback.print_exc()

                print()
                connector.rollback()
                raise


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]


def process_batch(rows):
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
    main()
