from util.PostGreConnector import PostGreConnector


def load_articles(ids):

    with PostGreConnector.from_configuration() as connector:
        cursor = connector.create_cursor()

        cursor.execute('select url, title from articles where id in (%s)' % ','.join('%s' for i in ids), ids)

        return cursor.fetchall()


if __name__ == "__main__":
    print(load_articles([52846, 39121]))