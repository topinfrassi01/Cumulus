import json

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

        for noun in nouns:
            if noun not in keywords.keys():
                keywords[noun] = []
            keywords[noun].append(article_id)

    result = {}
    with PostGreConnector.from_configuration() as connector:
        for kw in keywords.keys():
            select_cursor = connector.create_cursor()
            select_cursor.execute("select avgperday from keywords where text = %s", (kw,))
            average_per_day = select_cursor.fetchone()

            if average_per_day is None:
                average_per_day = 0
            else:
                average_per_day = float(average_per_day[0])

            today_total = len(keywords[kw])
            coeff = (today_total / average_per_day) if not average_per_day == 0 else 1

            if coeff > 1.30:
                result[kw] = ("{0:.2f}".format(coeff), today_total, keywords[kw])

    return sorted(result.items(), key=lambda x: x[1][0], reverse=True)


if __name__ == "__main__":
    dates = _get_all_article_dates()
    nouns = get_nouns_for_date(dates[0])

    print(nouns)
