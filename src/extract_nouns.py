from util.PostGreConnector import PostGreConnector
from nlp.TextBlobExtractor import TextBlobExtractor
import json


def main():

    batch_size = 1000

    select_query = "select id,content from articles limit %s offset %s"
    insert_query = "insert into nouns(article_id, content_json) values(%s, %s)"

    with PostGreConnector.from_configuration() as connector:
        count_cur = connector.create_cursor()

        count_cur.execute("select count(id) from articles")
        articles_count = count_cur.fetchone()[0]

        # Nifty trick from https://stackoverflow.com/a/17511341/2785479 to ceil a division
        for batch_num in range(-(-articles_count // batch_size)):
            batch_start = batch_num * batch_size
            batch_end = batch_start + batch_size

            select_cur = connector.create_cursor()

            select_cur.execute(select_query, (batch_end, batch_start))

            rows = select_cur.fetchall()

            try:
                insert_cur = connector.create_cursor()

                print("Starting batch {0} to {1}".format(batch_start, batch_end))

                for article in rows:
                    article_id = article[0]
                    content = article[1]

                    noun_phrases = TextBlobExtractor.extract_noun_phrases(content)
                    np_json = json.dumps(noun_phrases)

                    insert_cur.execute(insert_query, (article_id, np_json))

                connector.commit()
                print("Commited batch {0} to {1}".format(batch_start, batch_end))
            except:
                print("Batch {0} to {1} failed.".format(batch_start, batch_end))
                connector.rollback()
                raise
    pass


if __name__ == "__main__":
    main()
