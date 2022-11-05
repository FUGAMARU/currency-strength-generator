import datetime
import os

from constant import UTC
from currency_strength import generate_currency_strength
from file_operation import save_to_file
from data_operation import convert_to_chartjs_format


def main():
    target_date_str = input("通貨強弱データーを取得したい日付を入力してください(例: 2022-11-04): ")
    target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").replace(tzinfo=UTC)

    currency_strength_data = generate_currency_strength(target_date)
    save_to_file(f"{os.getcwd()}/Formatted.json", convert_to_chartjs_format(currency_strength_data))


if __name__ == "__main__":
    main()
