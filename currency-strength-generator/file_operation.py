import os
import json


def get_config() -> dict[str, str | int]:
    """ 設定ファイルから値を取得する

    Returns
    -------
    dict[str, str | int]
        設定
    """
    with open(f"{os.getcwd()}/config.json") as file:
        return json.load(file)


def save_to_file(path: str, data: list[any] | dict[any, any]) -> None:
    """ (デバッグ用) リストや辞書をjsonファイルにダンプする

    Parameters
    ----------
    path: str
        保存先ファイルパス (含拡張子)
    list | dict
        リストや辞書
    """

    with open(path, "w") as file:
        json.dump(data, file, indent=2)
