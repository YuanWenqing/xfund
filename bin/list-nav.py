#!/usr/bin/env python3
# coding: utf8
import argparse
import logging

from fundstrategy import daos
from fundstrategy import fund_apis
from fundstrategy import setups


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('code', help='fund code')
    parser.add_argument('--start', help='start date')
    parser.add_argument('--end', help='end date')

    return parser.parse_args()


def main():
    args = parse_args()

    # api = fund_apis.DoctorXiong()
    api = fund_apis.EastMoney()
    nav_list = api.get_nav_list(args.code, args.start, args.end)
    info = nav_list.info

    sql = setups.setup_sql()
    nav_dao = daos.NavDao(sql)
    for nav in nav_list.nav_list:
        nav_dao.insert_ignore(info, nav)
    logging.info(f'{info}: {len(nav_list)} items')


if __name__ == '__main__':
    setups.setup_logging()
    main()
