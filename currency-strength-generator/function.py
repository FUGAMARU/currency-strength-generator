import pytz
import datetime


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
