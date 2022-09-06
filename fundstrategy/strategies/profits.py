# coding: utf8
import numpy as np

EQUITY_DECIMALS = 3  # 份额小数位
VALUE_DECIMALS = 4  # 净值小数位
AMOUNT_DECIMALS = 2  # 金额小数位
RATE_DECIMALS = 4  # 收益率小数位


class ProfitRecord:
    def __init__(self):
        self.equities = 0  # 持仓份额
        # 收益率曲线：date,position_amount,profit_amount,profit_rate,position_cost
        self.profit_histories = []
        self.buy_amount = 0  # 累计买入金额
        self.buys = []  # 购买历史：date,amount,equity
        self.sell_amount = 0  # 累计赎回金额
        self.sells = []  # 赎回历史：date,amount,equity

    @property
    def position_amount(self):
        """持仓金额"""
        return self.profit_histories[-1][1]

    @property
    def position_cost(self):
        """持仓成本"""
        # if self.buy_amount <= self.sell_amount:
        #     return 0
        cost = self.buy_amount - self.sell_amount
        return np.around(cost, AMOUNT_DECIMALS)

    @property
    def equity_cost(self):
        """份额成本"""
        cost = self.position_cost
        if self.equities == 0 or cost == 0:
            return 0
        return np.around(cost / self.equities, decimals=VALUE_DECIMALS)

    def settle_profit(self, date, net_value):
        """当天结算收益"""
        position_amount = np.around(self.equities * net_value, decimals=AMOUNT_DECIMALS)
        position_cost = self.position_cost
        profit_amount = np.around(position_amount + self.sell_amount - self.buy_amount, AMOUNT_DECIMALS)
        if self.buy_amount == 0:
            profit_rate = 0
        else:
            profit_rate = profit_amount / self.buy_amount
        profit_rate = np.around(profit_rate, RATE_DECIMALS)
        self.profit_histories.append((date, position_amount, profit_amount, profit_rate, position_cost))

    def buy(self, date, net_value, amount):
        """买入"""
        amount = np.around(amount, AMOUNT_DECIMALS)
        equity = np.around(amount / net_value, decimals=EQUITY_DECIMALS)
        self.buy_amount = np.around(self.buy_amount + amount, AMOUNT_DECIMALS)
        self.equities = np.around(self.equities + equity, EQUITY_DECIMALS)
        self.buys.append((date, amount, equity))

    def sell(self, date, net_value, position):
        """赎回"""
        equity = np.around(self.equities * position, decimals=EQUITY_DECIMALS)
        amount = np.around(equity * net_value, AMOUNT_DECIMALS)
        self.sell_amount = np.around(self.sell_amount + amount, AMOUNT_DECIMALS)
        self.equities = np.around(self.equities - equity, EQUITY_DECIMALS)
        self.sells.append((date, amount, equity))

    @property
    def final_profit(self):
        profit_amount = np.around(self.position_amount + self.sell_amount - self.buy_amount, AMOUNT_DECIMALS)
        profit_rate = np.around(profit_amount / self.buy_amount, RATE_DECIMALS)
        return profit_amount, profit_rate

    def print_profits(self):
        print('-' * 60)
        tformat = '{:<10} | {:>10} | {:>10} | {:>10} | {:>10}'
        print(tformat.format('date', 'position', 'profit', 'rate', 'cost'))
        print('-' * 60)
        for date, position_amount, profit_amount, profit_rate, position_cost in self.profit_histories:
            profit_rate = f'{profit_rate * 100:.2f}%'
            print(tformat.format(date, position_amount, profit_amount, profit_rate, position_cost))
        print('-' * 60)

    def print_buys(self):
        self.do_print_ops('buy', self.buys)

    def print_sells(self):
        self.do_print_ops('sell', self.sells)

    def do_print_ops(self, op, op_histories):
        print('-' * 40)
        tformat = '{:<10} | {:>10} | {:>12}'
        print(tformat.format('date', 'amount', 'equity'))
        print('-' * 40)
        total_amount = 0
        total_equities = 0
        for date, amount, equity in op_histories:
            total_amount += amount
            total_equities += equity
            print(tformat.format(date, amount, equity))
        print('-' * 40)
        equities = np.around(total_equities, EQUITY_DECIMALS)
        print(tformat.format(op, total_amount, equities))

    def print_final(self):
        tformat = '{:<10} | {:>10}'
        print(tformat.format('buy', self.buy_amount))
        print(tformat.format('sell', self.sell_amount))
        print(tformat.format('position', self.position_amount))
        print('-' * 30)
        profit_amount, profit_rate = self.final_profit
        print(tformat.format('profit', profit_amount))
        print(tformat.format('rate', f'{profit_rate * 100:.2f}%'))
