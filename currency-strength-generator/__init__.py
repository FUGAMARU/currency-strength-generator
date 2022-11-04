import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import MetaTrader5 as mt5

import file_operation

if not mt5.initialize():
    print("MT5の初期化に失敗しました")
    print(mt5.last_error())
    mt5.shutdown()
    quit()

config = file_operation.get_config()

if not mt5.login(config["account"], password=config["password"], server=config["server"]):
    print("ユーザー認証に失敗しました")
    mt5.shutdown()
    quit()

print("MT5の準備が完了しました")
