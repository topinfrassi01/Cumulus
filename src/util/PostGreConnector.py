import psycopg2
from util.Global_Variables import app_config


class PostGreConnector():
    def __init__(self, host, dbname, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._dbname = dbname
        self._connection = None
        self._is_connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def connect(self):
        if self._is_connected:
            raise ConnectionError("Connection is already opened.")

        conn_string = "host={0} dbname='{1}' user='{2}' password='{3}'"\
            .format(self._host, self._dbname, self._username, self._password)

        self._connection = psycopg2.connect(conn_string)

        self._is_connected = True

    def create_cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        if "close" in dir(self._connection) and not self._connection.close:
            self._connection.close()

        self._is_connected = False

    # noinspection PyBroadException
    def test(self):
        try:
            self.connect()
            cur = self.create_cursor()
            cur.execute('SELECT 1')
            return True
        except :
            return False
        finally:
            self.close()

    @staticmethod
    def from_configuration():

        db_config = app_config["database"]

        return PostGreConnector(host=db_config["host"],
                                dbname=db_config["database_name"],
                                username=db_config["username"],
                                password=db_config["password"])


