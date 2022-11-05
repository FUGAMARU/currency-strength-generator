import math
import datetime
import MetaTrader5 as mt5

from constant import SYMBOLS, CURRENCIES, UTC
from mt5_api_function import get_latest_unixtime
from file_operation import get_config
from function import is_DST


def generate_currency_strength(target_datetime: datetime.datetime) -> dict[str, list[list[int | float]]]:
    """ 指定した日付の通貨強弱データーを作成する

    Parameters
    ----------
    target_datetime: datetime.date
        通貨強弱データーを作成したい日のdateオブジェクト

    Returns
    -------
    dict[str, list[list[int | float]]]
      1日分の通貨強弱データー
      {"USD": [[unixtime, 通貨強弱], [unixtime, 通貨強弱], ...], "EUR": [[unixtime, 通貨強弱], ...], "GBP": [...]}
    """

    base_unixtime = int(target_datetime.timestamp())

    day_end_unixtime = int(target_datetime.replace(hour=23, minute=55).timestamp())
    current_unixtime = get_latest_unixtime(mt5.TIMEFRAME_M5)

    goal_unixtime = current_unixtime if current_unixtime < day_end_unixtime else day_end_unixtime

    print(f"{target_datetime.date()}の通貨強弱データーを作成しています…")

    strength = {}  # 実際の通貨強弱データー格納先
    for currency in CURRENCIES:
        strength[currency] = []

    # v1(起点価格)の用意
    v1 = {}
    for symbol in SYMBOLS:
        v1[symbol] = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, base_unixtime, 1)[0]["open"]

    v2 = {}
    while True:
        # v2(現在価格)の用意
        for symbol in SYMBOLS:
            ohlc = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, base_unixtime, 1)

            # データー欠損チェック
            if not ohlc:
                print(f"{symbol}の{datetime.datetime.fromtimestamp(base_unixtime, UTC)}(MT5表示)の価格データーが欠損しているため通貨強弱データーを作成することができません")
                quit()

            v2[symbol] = ohlc[0]["open"]

        # v1は起点の価格、v2は現在時刻の価格
        EURUSD = getVal(v1["EURUSD"], v2["EURUSD"])
        USDJPY = getVal(v1["USDJPY"], v2["USDJPY"])
        USDCHF = getVal(v1["USDCHF"], v2["USDCHF"])
        GBPUSD = getVal(v1["GBPUSD"], v2["GBPUSD"])
        AUDUSD = getVal(v1["AUDUSD"], v2["AUDUSD"])
        USDCAD = getVal(v1["USDCAD"], v2["USDCAD"])
        NZDUSD = getVal(v1["NZDUSD"], v2["NZDUSD"])
        EURJPY = getValM(v1["EURUSD"], v2["EURUSD"], v1["USDJPY"], v2["USDJPY"])
        EURCHF = getValM(v1["EURUSD"], v2["EURUSD"], v1["USDCHF"], v2["USDCHF"])
        EURGBP = getValD(v1["EURUSD"], v2["EURUSD"], v1["GBPUSD"], v2["GBPUSD"])
        CHFJPY = getValD(v1["USDJPY"], v2["USDJPY"], v1["USDCHF"], v2["USDCHF"])
        GBPCHF = getValM(v1["GBPUSD"], v2["GBPUSD"], v1["USDCHF"], v2["USDCHF"])
        GBPJPY = getValM(v1["GBPUSD"], v2["GBPUSD"], v1["USDJPY"], v2["USDJPY"])
        AUDCHF = getValM(v1["AUDUSD"], v2["AUDUSD"], v1["USDCHF"], v2["USDCHF"])
        AUDJPY = getValM(v1["AUDUSD"], v2["AUDUSD"], v1["USDJPY"], v2["USDJPY"])
        AUDCAD = getValM(v1["AUDUSD"], v2["AUDUSD"], v1["USDCAD"], v2["USDCAD"])
        EURCAD = getValM(v1["EURUSD"], v2["EURUSD"], v1["USDCAD"], v2["USDCAD"])
        GBPCAD = getValM(v1["GBPUSD"], v2["GBPUSD"], v1["USDCAD"], v2["USDCAD"])
        GBPAUD = getValD(v1["GBPUSD"], v2["GBPUSD"], v1["AUDUSD"], v2["AUDUSD"])
        EURAUD = getValD(v1["EURUSD"], v2["EURUSD"], v1["AUDUSD"], v2["AUDUSD"])
        CADCHF = getValD(v1["USDCHF"], v2["USDCHF"], v1["USDCAD"], v2["USDCAD"])
        CADJPY = getValD(v1["USDJPY"], v2["USDJPY"], v1["USDCAD"], v2["USDCAD"])
        AUDNZD = getValD(v1["AUDUSD"], v2["AUDUSD"], v1["NZDUSD"], v2["NZDUSD"])
        EURNZD = getValD(v1["EURUSD"], v2["EURUSD"], v1["NZDUSD"], v2["NZDUSD"])
        GBPNZD = getValD(v1["GBPUSD"], v2["GBPUSD"], v1["NZDUSD"], v2["NZDUSD"])
        NZDCAD = getValM(v1["NZDUSD"], v2["NZDUSD"], v1["USDCAD"], v2["USDCAD"])
        NZDCHF = getValM(v1["NZDUSD"], v2["NZDUSD"], v1["USDCHF"], v2["USDCHF"])
        NZDJPY = getValM(v1["NZDUSD"], v2["NZDUSD"], v1["USDJPY"], v2["USDJPY"])

        # 各通貨の値の計算
        Pairs = 7

        # その時間における通貨ごとの通貨強弱
        values = {
            "EUR": (EURUSD + EURJPY + EURCHF + EURGBP + EURAUD + EURCAD + EURNZD) / Pairs,
            "USD": (-EURUSD + USDJPY + USDCHF - GBPUSD - AUDUSD + USDCAD - NZDUSD) / Pairs,
            "JPY": (-EURJPY - USDJPY - CHFJPY - GBPJPY - AUDJPY - CADJPY - NZDJPY) / Pairs,
            "CHF": (-EURCHF - USDCHF + CHFJPY - GBPCHF - AUDCHF - CADCHF - NZDCHF) / Pairs,
            "GBP": (-EURGBP + GBPUSD + GBPCHF + GBPJPY + GBPAUD + GBPCAD + GBPNZD) / Pairs,
            "AUD": (-EURAUD + AUDUSD + AUDJPY + AUDCHF - GBPAUD + AUDCAD + AUDNZD) / Pairs,
            "CAD": (-EURCAD - USDCAD + CADJPY + CADCHF - GBPCAD - AUDCAD - NZDCAD) / Pairs,
            "NZD": (-EURNZD + NZDUSD + NZDJPY + NZDCHF - GBPNZD + NZDCAD - AUDNZD) / Pairs
        }

        for currency, value in values.items():
            server_timezone = get_config()["serverTimezone"]
            unixtime = base_unixtime - 10800 if is_DST(base_unixtime, server_timezone) else base_unixtime - 7200
            strength[currency].append([unixtime, value])

        if base_unixtime == goal_unixtime:
            break

        base_unixtime += 300

    return strength


def getVal(v1, v2):
    if v2 == 0:
        return
    return math.log(v2 / v1) * 10000


def getValM(v1, v2, v3, v4):
    v1 = v1 * v3
    v2 = v2 * v4
    if v2 == 0:
        return
    return math.log(v2 / v1) * 10000


def getValD(v1, v2, v3, v4):
    if v3 == 0 or v4 == 0:
        return
    v1 = v1 / v3
    v2 = v2 / v4
    if v2 == 0:
        return
    return math.log(v2 / v1) * 10000
