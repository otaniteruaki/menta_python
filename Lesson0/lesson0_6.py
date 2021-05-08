def name_check(name):
  name_list=["たんじろう","ぎゆう","ねずこ","むざん"]
  check_result = name in name_list
  if check_result == True:
    print(name + "は存在します。")
  else:
    print(name + "は存在しません。")


name_check("たんじろう")