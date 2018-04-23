from util.PostGreConnector import PostGreConnector
import json


def create_keywords_average():
    with PostGreConnector.from_configuration() as connector:
        select_all = """select content_json, pubdate
                        from articles inner join keywords_per_article np on articles.id = np.article_id
                        order by pubdate """

        cursor = connector.create_cursor()
        cursor.execute(select_all)

        keywords_per_articles = cursor.fetchall()

    keywords_structure = {}
    for row in keywords_per_articles:
        keywords = json.loads(row[0], encoding="utf8")
        pubdate = row[1]

        for keyword in keywords:
            if keyword  not in keywords_structure.keys():
                keywords_structure[keyword] = Keyword(keyword, pubdate, pubdate, 1, 1)
            else:
                if not pubdate == keywords_structure[keyword].last_date:
                    keywords_structure[keyword].day_count += 1

                keywords_structure[keyword].last_date = pubdate
                keywords_structure[keyword].total += 1

    kw_to_remove = []
    for kw, value in keywords_structure.items():
        keywords_structure[kw].avg_per_day = (value.total / value.day_count)
        if value.total <= 3:
            kw_to_remove.append(kw)

    for kw in kw_to_remove:
        keywords_structure.pop(kw)

    with PostGreConnector.from_configuration() as connector:
        try:
            cursor = connector.create_cursor()

            inserted_values = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in [a.get_values_to_insert() for a in keywords_structure.values()])
            cursor.execute("insert into keywords(text, firstpubdate, lastpubdate, avgperday, daycount) VALUES " + inserted_values)

            connector.commit()
        except:
            connector.rollback()
            raise


class Keyword:

    def __init__(self, word, first_date, last_date, total, day_count):
        self.word = word
        self.first_date = first_date
        self.last_date = last_date
        self.total = total
        self.day_count = day_count
        self.avg_per_day = 0

    def get_values_to_insert(self):
        return self.word, self.first_date, self.last_date, self.avg_per_day, self.day_count


if __name__ == "__main__":
    create_keywords_average()