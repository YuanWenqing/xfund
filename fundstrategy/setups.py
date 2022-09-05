# coding: utf8
import logging
import logging.config
import os


def setup_logging(conf_file='logging.ini'):
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig(conf_file)
    logging.info(f'config log from file: {conf_file}')
