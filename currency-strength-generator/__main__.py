from currency_strength import generate_currency_strength
from file_operation import save_result
from data_operation import convert_to_chartjs_format
from function import check_validation


def main():
    target_date_str = input("通貨強弱データーを取得したい日付を入力してください(例: 2022-11-04): ")
    target_date = check_validation(target_date_str)

    currency_strength_data = generate_currency_strength(target_date)
    formatted_currency_strength_data = convert_to_chartjs_format(currency_strength_data)

    saved_files = save_result(currency_strength_data, formatted_currency_strength_data, target_date_str)

    print(f"通貨強弱データーを{len(saved_files)}件生成しました")
    for file_name in saved_files:
        print(file_name)


if __name__ == "__main__":
    main()
