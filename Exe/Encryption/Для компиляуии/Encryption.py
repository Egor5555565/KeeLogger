from sys import exit
alphabet = sorted('4ыhПЩm%ЗXd)мsЪ?UEюДОКЖЭo<етй;n|1нэYИuxСяп3РХ"6и►скЮТЦ+9гFцr$#&ЕЛvJyрkфЁшл-fjG5wъШSЙМgA@QуaZва7z2RГёУхФЯT^0щcplь\/iV.жW=чБдKбe№:ЬLbВOНDBCt8>_!*оЧqMзIHЫ (,PNА')

main_key = input("Введите основной ключ: ")
dop_key = 0
for value in main_key: dop_key += int(value)
key = int(main_key) + dop_key

def CodeBin(item):
	low, high = 0, 155
	while low <= high:
		mid = (low + high) // 2
		guess = alphabet[mid]
		if guess == item:
			return chr(mid + key)
		if guess > item:
			high = mid - 1
		else:
			low = mid + 1
	return item

def DeCodeBin(item):
	if (ord(item) - key) >= 0 and (ord(item) - key) <= 155:
		return alphabet[ord(item) - key]
	else:
		return item

def CodeLine(line):
	LineFinish = ""
	for elem in line:
		LineFinish += CodeBin(elem)
	return LineFinish

def DeCodeLine(line):
	LineFinish = ""
	for elem in line:
		LineFinish += DeCodeBin(elem)
	return LineFinish

while 1:
	choise = int(input("1. Зашифовать, 2. Рассшифровать,  !1 & !2 Выход: "))
	if (choise < 1) or (choise > 2):
		exit()
	LineStart = input("Введите стоку: ")
	if choise == 1:
		print(CodeLine(LineStart))
	else:
		print(DeCodeLine(LineStart))
		
input("Введите что-нибудь для выхода...")