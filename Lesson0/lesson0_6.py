def name_check(name):
  name_list=["たんじろう","ぎゆう","ねずこ","むざん"]
  if name in name_list:
    print(name + "は存在します。")
  else:
    print(name + "は存在しません。")


name_check("たんじろう")