from datetime import datetime
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する（chromedriverの格納場所を指定）
    # return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)
    # #Driver自動更新仕様の以下に変更
    return Chrome(ChromeDriverManager().install(), options=options)

#ログファイル出力の関数
LOG_FILE_PATH = "./log/log_{datetime}.log"
log_file_path = LOG_FILE_PATH.format(datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
def log(txt):
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt) #%構文での文字列の書式設定
    # ログ出力
    with open(log_file_path, 'a', encoding="utf-8_sig") as f:
        f.write(logStr + '\n')
    print(logStr)

#tableから対象（=target）の行を探す関数を定義
def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理
def main():
    #ログ出し
    log("処理開始")
    #検索ワードインプット
    search_keyword = input("検索するキーワードを指定してください >>> ")
    #ログ出し
    log("検索キーワード：{}".format(search_keyword))
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try: #例外が発生するかもしれないが、処理したい内容をtryに記載
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except: #例外が発生したら、exceptを実行
        pass

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # 企業名リスト
    exp_name_list = []
    # サブタイトルのリスト
    exp_copy_list = []
    # 雇用形態のリスト
    exp_status_list = []
    #　年収リスト
    exp_income_list = []

    #ログの失敗/成功カウント変数定義
    count = 0
    success = 0
    fail = 0

    while True: #次のページボタンが存在する限りループさせる
        # 検索結果の1ページ目の会社名を取得（新着だけ取得するために　.cassetteRecruitをつける）
        name_list = driver.find_elements_by_css_selector(".cassetteRecruit .cassetteRecruit__name")
        # 検索結果の1ページ目のサブタイトルを取得（新着だけ取得するために　.cassetteRecruitをつける）
        copy_list = driver.find_elements_by_css_selector(".cassetteRecruit .cassetteRecruit__copy")
        #検索結果の1ページ目のラベルリストを取得（新着だけ取得するために　.cassetteRecruitをつける）
        status_list = driver.find_elements_by_css_selector(".cassetteRecruit .labelEmploymentStatus")
        # 検索結果の1ページ目のテーブルを取得（新着だけ取得するために　.cassetteRecruitをつける）
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

        #１ページ分繰り返し処理
        for name, copy, status, table in zip(name_list, copy_list, status_list, table_list):
            try: #例外が発生するかもしれないが、処理したい内容をtryに記載
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                #年収の行を検索する
                income_list = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                exp_income_list.append(income_list)
                #ログ出し
                log(f"{count}件目成功:{name.text}") #f文字列
                #成功カウント
                success+=1
            except Exception as e: #例外が発生したら、exceptを実行
                #ログ出し
                log(f"{count}件目失敗 : {name.text}")
                log(e) # Exception（例外）の内容を表示
                fail+=1
            finally: # finallyは成功でのエラーでも必ず実行
                #ログ出し
                count+=1

        #次のページボタンがあればクリック、なければ終了
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft") #次へボタンの要素取得
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href") #next_page要素が複数存在するので１つ目を指定
            driver.get(next_page_link)
        else:
            break

    #CSVの定義
    EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
    #CSV出力時間
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # データフレームを作成
    df = pd.DataFrame({"企業名":exp_name_list,"キャッチコピー":exp_copy_list,"ステータス":exp_status_list,"年収":exp_income_list})
    #CSVに出力
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword,datetime=now), encoding="utf-8-sig")

    #ログ出し
    log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()