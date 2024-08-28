# coding: utf8
import logging
import re
import threading
import time
import typing

import pymysql
from pymysql import cursors


class ConnectionFactory:
    @staticmethod
    def parse_url(url: str):
        m = re.match('^mysql://(.+):(.+)@(.+)/(.+)$', url)
        if m is None:
            raise ValueError(f'illegal sql url: {url}, should be like `mysql://<user>:<password>@<host>/db`')
        user, password, host, db = m.group(1), m.group(2), m.group(3), m.group(4)
        return ConnectionFactory(host=host, user=user, password=password, database=db)

    def __init__(self, host, user, password, database):
        self.options = dict(
            host=host,
            user=user,
            password=password,
            database=database,

            cursorclass=cursors.DictCursor,
            autocommit=True,
            charset='utf8',
        )

    def __repr__(self):
        return f"<{self.__class__.__name__}: url={self.url()}>"

    def url(self):
        user, password = self.options['user'], self.options['password']
        host, database = self.options['host'], self.options['database']
        return f'mysql://{user}@{host}/{database}'

    def do_connect(self, **override_options) -> pymysql.Connection:
        if len(override_options) > 0:
            options = dict(self.options)
            options.update(override_options)
        else:
            options = self.options
        return pymysql.connect(**options)
        # return pymysql.connect(**self.options)


class Transaction:
    def __init__(self, conn: pymysql.Connection):
        self.conn = conn

    def __enter__(self):
        self.conn.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


class SqlHandler:
    def __init__(self, factory: ConnectionFactory):
        self.factory = factory
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sql_logger = logging.getLogger('sql')
        self.conn_locals = threading.local()

    def __repr__(self):
        return f"<{self.__class__.__name__}: url={self.factory.url()}>"

    @property
    def current_connection(self) -> typing.Optional[pymysql.Connection]:
        if hasattr(self.conn_locals, 'conn') and self.conn_locals.conn.open:
            return self.conn_locals.conn
        return None

    @current_connection.setter
    def current_connection(self, conn: pymysql.Connection):
        self.conn_locals.conn = conn

    def do_execute(self, cursor, query, args):
        beg = time.time()
        try:
            cursor.execute(query, args)
        finally:
            cost = time.time() - beg
            self.sql_logger.info(f'{self.__class__.__name__}: cost={cost:.3f}s, query={query}, args={args}')

    def do_insert(self, query, args, return_id=False):
        def do_execute():
            with conn.cursor() as cursor:
                self.do_execute(cursor, query, args)
                if return_id:
                    # get must before commit
                    insert_id = conn.insert_id()
                if return_id:
                    return insert_id

        conn = self.current_connection
        if conn is None:
            with self.factory.do_connect() as conn:
                return do_execute()
        else:
            return do_execute()

    def do_select(self, query, args=None, size: typing.Union[int, None] = 0, cursorclass=None):
        """
        :param query:
        :param args:
        :param size: None: 一个；0：全部；>=1 size个
        :param cursorclass:
        :return:
        """

        def do_execute():
            with conn.cursor(cursor=cursorclass) as cursor:
                self.do_execute(cursor, query, args)
                if size is None:
                    # 单独获取一个
                    return cursor.fetchone()
                elif size == 0:
                    # 获取全部
                    return cursor.fetchall()
                else:
                    assert size >= 1
                    return cursor.fetchmany(size)

        conn = self.current_connection
        if conn is None:
            with self.factory.do_connect() as conn:
                return do_execute()
        else:
            return do_execute()

    def do_update(self, query, args=None):
        def do_execute():
            with conn.cursor() as cursor:
                self.do_execute(cursor, query, args)

        conn = self.current_connection
        if conn is None:
            with self.factory.do_connect() as conn:
                return do_execute()
        else:
            return do_execute()

    def do_delete(self, query, args=None):
        def do_execute():
            with conn.cursor() as cursor:
                self.do_execute(cursor, query, args)

        conn = self.current_connection
        if conn is None:
            with self.factory.do_connect() as conn:
                return do_execute()
        else:
            return do_execute()

    def transaction(self, conn: pymysql.Connection = None) -> Transaction:
        if conn is None or not conn.open:
            conn = self.factory.do_connect(autocommit=False)
        self.current_connection = conn
        return Transaction(conn)
