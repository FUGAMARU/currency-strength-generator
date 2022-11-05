import datetime
import os

from constant import UTC
from currency_strength import generate_currency_strength
from file_operation import save_to_file


def main():
    target_date_str = input("通貨強弱データーを取得したい日付を入力してください(例: 2022-11-04): ")
    target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").replace(tzinfo=UTC)

    csd = generate_currency_strength(target_date)
    save_to_file(f"{os.getcwd()}/通貨強弱.json", csd)


if __name__ == "__main__":
    main()
