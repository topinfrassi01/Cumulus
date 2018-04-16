from util.PostGreConnector import PostGreConnector
import json


def get_all_dates():
    with PostGreConnector.from_configuration() as connector:
        select_cursor = connector.create_cursor()

        select_cursor.execute("select distinct pubdate from articles")

        return select_cursor.fetchall()




def main():
    with PostGreConnector.from_configuration() as connector:
        select_cursor = connector.create_cursor()

        select_cursor.execute("""select articles.id, content_json from articles
    inner join nouns_per_article on nouns.article_id = articles.id
    where articles.pubdate = '2017-01-01'
    """)

        data = select_cursor.fetchall()

    keywords = {}
    for row in data:
        nouns = json.loads(row[1], encoding="utf8")
        article_id = int(row[0])

        for noun in nouns :
            if noun not in keywords.keys():
                keywords[noun] = 0
            keywords[noun] += 1


    for key, value in keywords.items():
        if value > 2:
            print ("Noun {0} : {1}".format(key, value))


if __name__ == "__main__":
    main()