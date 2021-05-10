source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
  word = input("鬼滅の登場人物の名前を入力してください >>> ")

  ### ここに検索ロジックを書く
  if word in source:
    print("「{}」が見つかりました".format(word))
  else:
    print("「{}」が見つかりませんでした。".format(word))

if __name__ == "__main__":
  search()