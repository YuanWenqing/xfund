# xfund
基金和股票数据，以及一些买卖策略验证


# 基金&股票API

## 天天基金
基金实时净值：http://fundgz.1234567.com.cn/js/161725.js
~~~json
{
    "fundcode": "161725",
    "name": "招商中证白酒指数(LOF)A",
    "jzrq": "2021-12-21",
    "dwjz": "1.3768",
    "gsz": "1.3797",
    "gszzl": "0.21",
    "gztime": "2021-12-22 15:00"
}
~~~

基金历史净值：https://fund.eastmoney.com/pingzhongdata/001186.js

基金名称列表：https://fund.eastmoney.com/js/fundcode_search.js

基金公司列表：https://fund.eastmoney.com/js/jjjz_gs.js

## 新浪财经
股票实时行情：http://hq.sinajs.cn/list=sh600519
~~~
贵州茅台,2040.000,2038.200,2048.000,2063.000,2040.000,2047.980,2048.000,1743079,3570928372.000,100,2047.980,200,2047.970,100,2047.360,700,2047.340,300,2046.500,919,2048.000,200,2048.010,4000,2048.140,500,2048.630,500,2048.830,2021-12-22,15:00:03,00,
~~~
字段解释：
~~~
0：”贵州茅台”，股票名字；
1：”27.55″，今日开盘价；
2：”27.25″，昨日收盘价；
3：”26.91″，当前价格；
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手；
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2008-01-11″，日期；
31：”15:05:32″，时间；
~~~

股票日K数据：http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600519&scale=240&ma=no&datalen=1023
~~~json
[
    {
        "day": "2020-05-14",
        "open": "1330.000",
        "high": "1334.880",
        "low": "1325.110",
        "close": "1326.590",
        "volume": "1857492"
    },
    {
        "day": "2020-05-15",
        "open": "1329.000",
        "high": "1333.500",
        "low": "1301.880",
        "close": "1313.000",
        "volume": "2639808"
    },
    ...
]
~~~

股票分时数据（分钟级）：https://cn.finance.sina.com.cn/minline/getMinlineData?symbol=sz000712
~~~json
{
    "result": {
        "status": {
            "code": 0,
            "msg": "LocalCache:success"
        },
        "data": [
            {
                "m": "09:25:00",
                "v": "3975466",
                "p": "12.98",
                "avg_p": "12.98"
            },
            {
                "m": "09:30:00",
                "v": "1656300",
                "p": "12.98",
                "avg_p": "12.98"
            },
            {
                "m": "09:31:00",
                "v": "182000",
                "p": "12.98",
                "avg_p": "12.98"
            },
            ...
            {
                "m": "14:55:00",
                "v": "84200",
                "p": "12.98",
                "avg_p": "12.969"
            },
            {
                "m": "14:56:00",
                "v": "78300",
                "p": "12.98",
                "avg_p": "12.969"
            },
            {
                "m": "15:00:00",
                "v": "190100",
                "p": "12.98",
                "avg_p": "12.969"
            }
        ]
    }
}
~~~

## 腾讯财经
股票实时行情：http://qt.gtimg.cn/q=sh600519
~~~
v_sh600519="1~贵州茅台~600519~1386.16~1421.28~1418.00~32038~12201~19838~1386.16~20~1386.15~9~1386.13~23~1386.12~7~1386.11~9~1386.18~2~1386.19~3~1386.20~17~1386.23~13~1386.24~5~~20240801155903~-35.12~-2.47~1420.00~1384.70~1386.16/32038/4470988088~32038~447099~0.26~22.32~~1420.00~1384.70~2.48~17412.91~17412.91~8.67~1563.41~1279.15~0.86~28~1395.53~18.09~23.30~~~0.70~447098.8088~0.0000~0~ ~GP-A~-18.23~-3.10~3.61~32.54~28.33~1856.54~1361.30~-7.44~-6.70~-20.02~1256197800~1256197800~25.93~-21.33~1256197800~~~-24.25~0.00~~CNY~0~___D__F__N~1386.10~186";
~~~

## 雪球
股票实时行情：https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH600519,SZ300750
~~~json
{
    "data": [
        {
            "symbol": "SZ300750",
            "current": 180.3,
            "percent": -3.23,
            "chg": -6.01,
            "timestamp": 1722497676000,
            "volume": 23012659,
            "amount": 4180640117,
            "market_capital": 793104942127,
            "float_market_capital": 702242264908,
            "turnover_rate": 0.59,
            "amplitude": 3.17,
            "open": 185,
            "last_close": 186.31,
            "high": 186,
            "low": 180.1,
            "avg_price": 181.667,
            "trade_volume": 0,
            "side": 1,
            "is_trade": false,
            "level": 1,
            "trade_session": null,
            "trade_type": null,
            "current_year_percent": 12.05,
            "trade_unique_id": "23012659",
            "type": 11,
            "bid_appl_seq_num": null,
            "offer_appl_seq_num": null,
            "volume_ext": 900,
            "traded_amount_ext": 162270,
            "trade_type_v2": null,
            "yield_to_maturity": null
        },
        {
            "symbol": "SH600519",
            "current": 1386.16,
            "percent": -2.47,
            "chg": -35.12,
            "timestamp": 1722495600000,
            "volume": 3203810,
            "amount": 4470988088.03,
            "market_capital": 1741291142448,
            "float_market_capital": 1741291142448,
            "turnover_rate": 0.26,
            "amplitude": 2.48,
            "open": 1418,
            "last_close": 1421.28,
            "high": 1420,
            "low": 1384.7,
            "avg_price": 1395.5222338496976,
            "trade_volume": null,
            "side": null,
            "is_trade": false,
            "level": 2,
            "trade_session": null,
            "trade_type": null,
            "current_year_percent": -18.03,
            "trade_unique_id": null,
            "type": 11,
            "bid_appl_seq_num": null,
            "offer_appl_seq_num": null,
            "volume_ext": null,
            "traded_amount_ext": null,
            "trade_type_v2": null,
            "yield_to_maturity": null
        }
    ],
    "error_code": 0,
    "error_description": null
}
~~~

# 参考
* https://blog.csdn.net/qq1130169218/article/details/122087853
* https://cloud.tencent.com/developer/article/1695640
* https://blog.csdn.net/begin_python/article/details/126982865
* https://www.cnblogs.com/insane-Mr-Li/p/15378971.html
