import pytz
import datetime
import MetaTrader5 as mt5

from constant import UTC
from mt5_api_function import get_latest_unixtime


def is_DST(unixtime: int, timezone: str) -> bool:
    """ 指定したタイムゾーンが指定したUnixtime時点でサマータイムかどうか判定する

    Parameters
    ----------
    unixtime: int
        Unixtime
    timezone: str
        タイムゾーン

    Returns
    -------
    bool
        サマータイムかどうか
    """

    tz = pytz.timezone(timezone)
    if datetime.datetime.fromtimestamp(unixtime, tz).dst():
        return True

    return False


def is_open_market(unixtime: int) -> bool:
    """ 指定したUnixtime時点で外為市場がオープンしているか判定する

    土日と元日の場合Falseになる

    Parameters
    ----------
    unixtime: int
        Unixtime

    Returns
    -------
    bool
        指定したUnixtime時点で外為市場がオープンしているかどうか
    """

    date = datetime.datetime.fromtimestamp(unixtime, UTC).date()

    # 土日チェック
    weekday = date.weekday()
    if weekday >= 5:
        return False

    # 元日チェック
    if date.month == 1 and date.day == 1:
        return False

    return True


def check_validation(target_date_str: str) -> datetime.datetime:
    """ 入力された日付文字列をバリデーションチェックして問題なければdatetimeオブジェクトを生成する

    問題がある場合スクリプトを終了する

    Parameters
    ----------
    target_date_str: str
        日付文字列

    Returns
    -------
    datetime.datetime
        日付文字列を元に生成したdatetimeオブジェクト
    """

    # フォーマットチェック
    try:
        datetime.datetime.strptime(target_date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError:
        print("入力された日付のフォーマットが不正です")
        mt5.shutdown()
        quit()

    target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    target_date_unixtime = int(target_date.timestamp())

    # 休場チェック
    if not is_open_market(target_date_unixtime):
        print(f"{target_date_str}は土日か元日のため外為市場は休場しています")
        mt5.shutdown()
        quit()

    # 時空チェック
    latest_unixtime = get_latest_unixtime(mt5.TIMEFRAME_M5)

    if target_date_unixtime > latest_unixtime:
        print("指定する日付は現在よりも過去である必要があります")
        mt5.shutdown()
        quit()

    return target_date
