import re
phone = '+55 (11)A98167-.7677'
phone = re.sub('[^0-9^+]','',phone)
print(phone)