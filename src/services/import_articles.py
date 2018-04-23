from util.PostGreConnector import PostGreConnector
import pandas as pd
import os
from dateutil import parser


def import_articles(directory):
    insert_pub = "INSERT INTO publications(name) VALUES(%s) RETURNING publications.id;"
    insert_articles = """INSERT INTO articles(publicationid, author, pubdate, title, url, content)
        VALUES(%s, %s, %s, %s, %s, %s);"""

    csv_files = ["articles1.csv", "articles2.csv", "articles3.csv"]

    inserted_publications = {}

    with PostGreConnector.from_configuration() as connector:
        try:
            cursor = connector.create_cursor()
            for csv in csv_files:
                file_path = directory + csv
                if not os.path.isfile(file_path):
                    raise FileNotFoundError("File '{0}' doesn't exist".format(file_path))

                data = pd.read_csv(file_path)

                # Import publications
                for publication in data["publication"].unique():
                    if publication in inserted_publications.keys():
                        continue

                    cursor.execute(insert_pub, (publication,))
                    new_id = cursor.fetchone()[0]
                    inserted_publications[publication] = new_id

                connector.commit()

                cursor = connector.create_cursor()

                # CSV are under this format : id, title, publication, author, date, year, month, url, content
                for index, row in data.iterrows():
                    pub_id = inserted_publications[row["publication"]]

                    # If date doesn't work, the row can't be used.
                    try:
                        dt = parser.parse(row["date"])
                    except:
                        continue

                    cursor.execute(insert_articles, (pub_id, row["author"],
                                                     dt, row["title"],
                                                     row["url"], row["content"]))

                connector.commit()
        except:
            connector.rollback()
            raise


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, '../data/all-the-news/')
    import_articles(filepath)
