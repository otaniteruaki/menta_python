### 検索ツール
def search():
  with open("Lesson1/data/source.csv", "r", encoding="utf-8") as f:
    for row in f:
      csv_rows = row.strip().split(',')
      word = input("鬼滅の登場人物の名前を入力してください >>> ")

      ### ここに検索ロジックを書く
      if word in csv_rows:
        print("「{}」が見つかりました".format(word))
      else:
        print("「{}」が見つかりませんでした。キャラクターリストに追加しました↓↓".format(word))
        #csv_rowsにwordを追加して表示
        csv_rows.append(word)
        print("キャラクターリスト=" + str(csv_rows))

if __name__ == "__main__":
  search()