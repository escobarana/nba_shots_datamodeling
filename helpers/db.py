import pandas as pd
import psycopg2


class Database:
    """
    Database class for connecting to a PostgreSQL database and executing queries.
    """

    def __init__(self, dbname: str, host: str, user: str, password: str):
        self.dbname = dbname
        self.host = host
        self.user = user
        self.password = password
        self.cur = None
        self.conn = None

    def create_database(self, database_name: str):
        conn = psycopg2.connect(
            dbname=self.dbname, host=self.host, user=self.user, password=self.password
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        cur.execute("DROP DATABASE IF EXISTS {};".format(database_name))
        cur.execute("CREATE DATABASE {};".format(database_name))

        conn.close()

        self.conn = psycopg2.connect(
            dbname=database_name, host=self.host, user=self.user, password=self.password
        )
        self.cur = self.conn.cursor()

    def drop_database(self, database_name: str):
        self.cur.execute("DROP DATABASE IF EXISTS {}".format(database_name))
        self.conn.commit()

    def drop_tables(self, drop_table_queries: list):
        for query in drop_table_queries:
            self.cur.execute(query)
        self.conn.commit()

    def create_tables(self, create_table_queries: list):
        for query in create_table_queries:
            self.cur.execute(query)
        self.conn.commit()

    def insert_data(self, query: str, data: pd.DataFrame):
        for i, row in data.iterrows():
            self.cur.execute(query, list(row))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
