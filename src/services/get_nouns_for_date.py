import json
import operator

from util.PostGreConnector import PostGreConnector


def _get_all_article_dates():
    with PostGreConnector.from_configuration() as connector:
        select_cursor = connector.create_cursor()

        select_cursor.execute("select distinct pubdate from articles")

        return select_cursor.fetchall()


def get_nouns_for_date(date):
    with PostGreConnector.from_configuration() as connector:
        select_cursor = connector.create_cursor()

        select_cursor.execute("""select articles.id, content_json from articles
    inner join nouns_per_article on nouns_per_article.article_id = articles.id
    where articles.pubdate = %s
    """, date)

        data = select_cursor.fetchall()

    keywords = {}
    for row in data:
        nouns = json.loads(row[1], encoding="utf8")
        article_id = int(row[0])

        for noun in nouns :
            if noun not in keywords.keys():
                keywords[noun] = []
            keywords[noun].append(article_id)

    return {k: v for k, v in keywords.items() if len(v) > 2}


if __name__ == "__main__":
    dates = _get_all_article_dates()
    nouns = get_nouns_for_date(dates[0])
    nouns = sorted(nouns.items(), key=lambda x : len(x[1]))
    nouns.reverse()

    print(nouns[0:10])

    #print(get_nouns_for_date(dates[0]))
