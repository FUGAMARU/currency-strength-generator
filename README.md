# currency-strength-generator

## ℹ️概要
  指定した日付の5分毎・1日分の通貨強弱データーを作成し、JSONやHTML(グラフ)を出力します。

  通貨強弱グラフを提供しているWebサービスは、よく知られているものでもいくつか存在しますが[^1]、どのサービスも軒並み前日分までの通貨強弱データーしか提供していません。

  currency-strength-generatorは、[MT5用Pythonライブラリー](https://pypi.org/project/MetaTrader5/)を介して過去の価格データーを取得、それを基に通貨強弱を計算することで、一昨日、またはそれ以前まで遡って通貨強弱データーを閲覧することを可能にします。

## 🛠️使い方
  ### ⚠️注意事項
  - MT5がそもそもWindowsソフトということもあり、MT5用PythonライブラリーもWindows環境でのみ使用可能となっています。  
  そのため、Pythonではありますがcurrency-strength-generatorは<u>**Windows環境でのみ使用可能**</u>です[^2]。
  - MT5から価格データーを取得する都合上、MT5にログイン可能なFX口座が必要となります(デモ口座可)
  - 理論上は過去のどの日にでも遡って通貨強弱データーを作成できますが、MT5の内部的な問題のせいか**2019年末頃以前**の日付を入力すると正常な通貨強弱データーが生成されない問題を確認しています。[^3]

  ### セットアップ
  (カレントディレクトリーは既にプロジェクトルートに移動済みのものとします)  

  **0. 必要であれば仮想環境を作成します**
  ```shell
    $ python -m venv venv
  ```
  **1. 依存ライブラリー一覧をインストールします**
  ```shell
    $ pip install -r requirements.txt
  ```
  **2. プロジェクトルートにある`config.json`を編集します**
  ```json
    {
        "account": 1234567,
        "password": "password",
        "server": "Axiory-Demo",
        "serverTimezone": "America/New_York"
    }
  ```
  MT5の口座番号を`account`に、MT5の口座パスワードを`password`に、接続先MT5サーバー名を`server`にそれぞれ記載します。

  `serverTimezone`は、自分が使う口座のブローカーがサマータイムの切り替えに採用しているタイムゾーンを[pytzの形式](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)で指定します。  
  大体のブローカー(日本含)はニューヨーク時間を採用しているので`"America/New_York"`を指定しますが、XMだとロンドン時間を採用しているので`"Europe/London"`と指定します。  
  ※タイムゾーンを間違えて指定しても動作に深刻な影響が及ぶことはありません。

  ### 実行
  ```shell
    $ ./venv/Scripts/activate # セットアップの項で仮想環境を作成した場合
    $ python -m currency-strength-generator
  ```
  コマンドを実行するとMT5が自動的に起動します
  ```shell
    MT5の準備が完了しました
    通貨強弱データーを取得したい日付を入力してください(例: 2022-11-04):
  ```
  MT5の起動・認証が完了するとこのようなプロンプトが表示されるので、欲しい通貨強弱データーの日付を指定します。

  ただし、  
  - `2022-5-5`や`2022/05/05`といったフォーマット不正
  - 土日や元日などの外為市場休場日
  - 現在より未来の日付

  といった日付を入力した場合、エラーメッセージを出力してプログラムは終了します。

  ### 作成されたデーターの確認
  ```shell
    通貨強弱データーを取得したい日付を入力してください(例: 2022-11-04): 2022-11-04
    2022-11-04の通貨強弱データーを作成しています…
    通貨強弱データーを2件生成しました
    D:\Desktop\currency-strength-generator/results/json/2022-11-04.json
    D:\Desktop\currency-strength-generator/results/html/2022-11-04.html
  ```
  通貨強弱データーの作成が完了すると、最後に、作成したファイルのフルパスをそれぞれ出力します。  
  プロジェクトルートに`results`フォルダーが作成され、その中でJSONファイルとHTMLファイル(グラフ)に分けてファイルが保存される仕様です。

  #### JSONファイル
  ```json
    {
    "EUR": [
        [
            1667509200,
            0.0
        ],
        [
            1667509500,
            2.412531687596828
        ],...

    ],
    "USD": ...

    }
  ```
  JSONファイルには、通貨ごとのキーがあり、それぞれに5分毎・1日分のUnixtimeスタンプと通貨強弱データーが配列として入っています。

  #### HTMLファイル(グラフ)
  ![generated graph](https://user-images.githubusercontent.com/7829486/200116955-be765697-0d49-48f9-a3f8-fbba568eba7a.jpg)
  HTMLファイルを開くと、[Chart.js](https://www.chartjs.org/)を使用して生成したグラフが確認できるようになっています。
  ホバーするとその時点での各通貨の通貨強弱がTooltipで表示されます。

## 通貨強弱の計算ロジックについて
  currency-strength-generatorでは、[以前Currency Strength Chartにて公開されていたPHPで記述された通貨強弱計算用ロジック](http://web.archive.org/web/20210316121139/https://currency-strength.com/about.html)を、Python用に独自にリファクタリングしたものを使用しています。

[^1]: [Currency Strength Chart](https://currency-strength.com/)、[通貨の強弱チャート(OANDAラボ)](https://www.oanda.jp/lab-education/oanda_lab/oanda_rab/currency_power_balance/)、[通貨強弱チャート(FX-labo)](https://fx-labo.app/strength/?t=today)など

[^2]: 一応[Linux上で動かせるMT5用Pythonライブラリー](https://pypi.org/project/mt5linux/)も存在するようですが、検証はしていません。

[^3]: MT5に元から入っているOHLCのデーターセットはMetaQuotes社のものですが、過去のデーターは値が抜けていたりとデーターセットとしての品質がそこまで高くないので、もしかするとブローカーが提供しているOHLCのデーターセットに切り替えるとうまくいくようになるかもしれませんが、未検証です。