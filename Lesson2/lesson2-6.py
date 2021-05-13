from datetime import datetime
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

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
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

#tableから対象（=target）の行を探す関数を定義
def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理
def main():
    search_keyword = input("検索するキーワードを指定してください >>> ")
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
            except: #例外が発生したら、exceptを実行
                pass

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


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()