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
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
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
    # 検索結果の1ページ目の会社名を取得（新着だけ取得するために　.cassetteRecruitをつける）
    name_list = driver.find_elements_by_css_selector(".cassetteRecruit .cassetteRecruit__name")
    # 検索結果の1ページ目のサブタイトルを取得（新着だけ取得するために　.cassetteRecruitをつける）
    copy_list = driver.find_elements_by_css_selector(".cassetteRecruit .cassetteRecruit__copy")
    #検索結果の1ページ目のラベルリストを取得（新着だけ取得するために　.cassetteRecruitをつける）
    status_list = driver.find_elements_by_css_selector(".cassetteRecruit .labelEmploymentStatus")
    # 検索結果の1ページ目のテーブルを取得（新着だけ取得するために　.cassetteRecruitをつける）
    table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

    for name, copy, status, table in zip(name_list, copy_list, status_list, table_list):
        exp_name_list.append(name.text)
        exp_copy_list.append(copy.text)
        exp_status_list.append(status.text)
        #年収の行を検索する
        income_list = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
        exp_income_list.append(income_list)

    # 1ページ分繰り返し
    for name, copy, status, income in zip(exp_name_list, exp_copy_list, exp_status_list, exp_income_list):
        print(name)
        print(copy)
        print(status)
        print(income)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()