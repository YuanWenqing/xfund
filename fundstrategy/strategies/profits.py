# coding: utf8
import numpy as np

EQUITY_DECIMALS = 3  # 份额小数位
VALUE_DECIMALS = 4  # 净值小数位
AMOUNT_DECIMALS = 2  # 金额小数位
RATE_DECIMALS = 4  # 收益率小数位


class ProfitRecord:
    def __init__(self):
        self.equities = 0  # 持仓份额
        self.profit_histories = []  # 收益率曲线：date,amount,profit_rate
        self.buy_amount = 0  # 累计买入金额
        self.buys = []  # 购买历史：date,amount,equity
        self.sell_amount = 0  # 累计赎回金额
        self.sells = []  # 赎回历史：date,amount,equity

    @property
    def position_amount(self):
        """持仓金额成本"""
        if self.buy_amount <= self.sell_amount:
            return 0
        return self.buy_amount - self.sell_amount

    @property
    def position_value(self):
        """持仓净值成本"""
        amount = self.position_amount
        if self.equities == 0 or amount == 0:
            return 0
        return np.around(amount / self.equities, decimals=VALUE_DECIMALS)

    def settle_profit(self, date, net_value):
        """当天结算收益"""
        amount = np.around(self.equities * net_value, decimals=AMOUNT_DECIMALS)
        position_amount = self.position_amount
        if position_amount == 0:
            profit_rate = 0
        else:
            profit_rate = amount / position_amount - 1
        profit_rate = np.around(profit_rate, RATE_DECIMALS)
        self.profit_histories.append((date, amount, profit_rate))

    def buy(self, date, amount, net_value):
        """买入"""
        amount = np.around(amount, AMOUNT_DECIMALS)
        equity = np.around(amount / net_value, decimals=EQUITY_DECIMALS)
        self.buy_amount += amount
        self.equities += equity
        self.buys.append((date, amount, equity))

    def sell(self, date, position, net_value):
        """赎回"""
        equity = np.around(self.equities * position, decimals=EQUITY_DECIMALS)
        amount = np.around(equity * net_value, AMOUNT_DECIMALS)
        self.sell_amount += amount
        self.equities -= equity
        self.sells.append((date, amount, equity))
