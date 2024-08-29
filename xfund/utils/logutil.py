# coding: utf8
import logging
import logging.config
import os
import sys


def setup_logging(conf_file='logging.ini'):
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig(conf_file)
    logging.info(f'config log from file: {conf_file}')


def change_log_level(level):
    logging.root.setLevel(level)
    for h in logging.root.handlers:
        h.setLevel(level)


def enable_debug_log():
    change_log_level(logging.DEBUG)


def console_handler():
    for handler in logging.root.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            return handler
    return None


class ConsoleDisableSession:
    def __init__(self, upgrade_level: int = logging.WARNING):
        self.handler = console_handler()
        self.upgrade_level = upgrade_level
        assert self.handler
        self.old_level = self.handler.level

    def __enter__(self):
        self.handler.setLevel(self.upgrade_level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handler.setLevel(self.old_level)


def disable_console_session():
    return ConsoleDisableSession()
