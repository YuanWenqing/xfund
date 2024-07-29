# coding: utf8
import logging
import logging.config
import os

from xfund.core import sql_handler


def setup_logging(conf_file='logging.ini'):
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig(conf_file)
    logging.info(f'config log from file: {conf_file}')


def setup_sql(mysql_url: str = 'mysql://fund:123456@localhost/fund'):
    factory = sql_handler.ConnectionFactory.parse_url(url=mysql_url)
    return sql_handler.SqlHandler(factory)
