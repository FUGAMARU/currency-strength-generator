import MetaTrader5 as mt5


def get_latest_unixtime(timeframe) -> int:
    """ 関数実行時点で取得可能な指定したタイムフレームの最も新しいUnixtimeを取得する

    Parameters
    ----------
    timeframe
        MT5ライブラリで定義されているタイムフレーム定数

    Returns
    -------
    int
        関数実行時点で取得可能な指定したタイムフレームの最も新しいUnixtime
    """

    return int(mt5.copy_rates_from_pos("EURUSD", timeframe, 0, 1)[0]["time"])
