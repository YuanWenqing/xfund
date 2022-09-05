# coding: utf8
import logging
import logging.config


def setup_logging(conf_file='logging.ini'):
    logging.config.fileConfig(conf_file)
    logging.info(f'config log from file: {conf_file}')
