import os
import json

from constant import ROOT_DIR
from data_operation import generate_chartjs_html


def get_config() -> dict[str, str | int]:
    """ 設定ファイルから値を取得する

    Returns
    -------
    dict[str, str | int]
        設定
    """
    with open(f"{ROOT_DIR}/config.json") as file:
        return json.load(file)


def save_result(data: dict[str, list[list[int | float]]], formattedData: dict[str, list[str] | dict[str, list[float]]], target_date_str: str) -> list[str]:
    """ 結果をファイルに保存する

    Parameters
    ----------
    data: dict[str, list[list[int | float]]]
        1日分の通貨強弱データー
        {"USD": [[unixtime, 通貨強弱], [unixtime, 通貨強弱], ...], "EUR": [[unixtime, 通貨強弱], ...], "GBP": [...]}
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
    list[str]
        保存したファイルのパス一覧
    """

    # 保存先ディレクトリーの作成
    os.makedirs(f"{ROOT_DIR}/results", exist_ok=True)
    os.makedirs(f"{ROOT_DIR}/results/json", exist_ok=True)
    os.makedirs(f"{ROOT_DIR}/results/html", exist_ok=True)

    json_file_path = f"{ROOT_DIR}/results/json/{target_date_str}.json"
    html_file_path = f"{ROOT_DIR}/results/html/{target_date_str}.html"

    save_to_file(json_file_path, data)

    with open(html_file_path, "w") as file:
        content = generate_chartjs_html(formattedData, target_date_str)
        file.write(content)

    return [json_file_path, html_file_path]


def save_to_file(path: str, data: list[any] | dict[any, any]) -> None:
    """ リストや辞書をJSONファイルに保存する

    Parameters
    ----------
    path: str
        保存先ファイルパス (含拡張子)
    list | dict
        リストや辞書
    """

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
