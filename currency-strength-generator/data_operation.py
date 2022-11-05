import datetime
import json

from constant import JST, CURRENCIES, ROOT_DIR


def convert_to_chartjs_format(currency_strength: dict[str, list[list[int | float]]]) -> dict[str, list[str] | dict[str, list[float]]]:
    """ 生成した通貨強弱データーをChart.jsで読み込むデーターフォーマットに変換する

    Parameters
    ----------
    currency_strength: dict[str, list[list[int | float]]]
        生成した1日分の通貨強弱データー
        {"USD": [[unixtime, 通貨強弱], [unixtime, 通貨強弱], ...], "EUR": [[unixtime, 通貨強弱], ...], "GBP": [...]}

    Returns
    -------
    dict[str, list[str] | dict[str, list[float]]]
        Chart.jsで読み込むデーターフォーマット
        ※時刻はJST表記に変換する
        {
            "x": ["2022-11-04T06:00:00", "2022-11-04T06:05:00", ...],
            "y": {
                "EUR": [通貨強弱, 通貨強弱, ...],
                "USD": [...],
                ...
            }
        }
    """

    output = {"x": [], "y": {}}

    # X軸(時系列)の用意
    for data in currency_strength["USD"]:
        unixtime = data[0]
        dt = datetime.datetime.fromtimestamp(unixtime, JST)
        output["x"].append(f"{dt.date()}T{dt.time()}")

    # Y軸(通貨強弱)の用意
    for currency in CURRENCIES:
        output["y"][currency] = []

    for currency, historicalData in currency_strength.items():
        for data in historicalData:
            output["y"][currency].append(data[1])

    return output


def generate_chartjs_html(formattedData: dict[str, list[str] | dict[str, list[float]]], target_date_str: str) -> str:
    """ Chart.js用に変換された通貨強弱データーを使ってHTMLソースを生成する

    Parameters
    ----------
    formattedData: dict[str, list[str] | dict[str, list[float]]]
        1日分の通貨強弱データーをChart.jsで読み込むデーターフォーマットに変換したもの
        {
            "x": ["2022-11-04T06:00:00", "2022-11-04T06:05:00", ...],
            "y": {
                "EUR": [通貨強弱, 通貨強弱, ...],
                "USD": [...],
                ...
            }
        }
    target_date_str: str
        指定した日付の文字列

    Returns
    -------
    str
        通貨強弱データーをChart.jsで表示するHTMLソース
    """

    with open(f"{ROOT_DIR}/currency-strength-generator/static/chartjs-template.html") as file:
        source = file.read()

        source = source.replace("!DATE", f"{target_date_str}")
        source = source.replace("!UNIXTIME_LIST", json.dumps(formattedData["x"]))

        source = source.replace("!USD_VALUES", json.dumps(formattedData["y"]["USD"]))
        source = source.replace("!EUR_VALUES", json.dumps(formattedData["y"]["EUR"]))
        source = source.replace("!JPY_VALUES", json.dumps(formattedData["y"]["JPY"]))
        source = source.replace("!GBP_VALUES", json.dumps(formattedData["y"]["GBP"]))
        source = source.replace("!AUD_VALUES", json.dumps(formattedData["y"]["AUD"]))
        source = source.replace("!CHF_VALUES", json.dumps(formattedData["y"]["CHF"]))
        source = source.replace("!CAD_VALUES", json.dumps(formattedData["y"]["CAD"]))
        source = source.replace("!NZD_VALUES", json.dumps(formattedData["y"]["NZD"]))

        return source
