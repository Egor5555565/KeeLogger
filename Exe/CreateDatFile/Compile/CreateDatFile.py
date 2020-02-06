from pickle import dump

def CreateMass(name):
	if name not in names_mass:
		globals()[name] = []
		names_mass.append(name)
		return name
	return FillingOutFile()

def InputType():
	Type = CheckValue(input("Введите тип данных(int, str): "), "Введите тип данных(int, str): ")
	if (Type == "str") or (Type == "int"):
		return Type
	else:
		return InputType()

def InputValue(Type):
	Value = CheckValue(input("Введите значение: "), "Введите значение: ")
	try:
		if Type == "int":
			value = int(Value)
			return Value
		else:
			return Value
	except:
		return InputValue(Type)

def CheckValue(Value, string):
	if Value != "":
		return Value
	else:
		Value = input(string)
		return CheckValue(Value, string)

def CheckValueForChoise(Value, string):
	if (Value == "0") or (Value == "1"):
		return Value
	else:
		Value = input(string)
		return CheckValueForChoise(Value, string)

def FillingOutFile():
	name_mass = CreateMass(CheckValue(input("Введите имя массива: "), "Введите имя массива: "))
	choise = True
	while choise:
		Type = InputType()
		Value = InputValue(Type)
		globals()[name_mass].append(Value if Type == "str" else int(Value))
		choise = int(CheckValueForChoise(input("Ввести еще значение(0 или 1)? "), "Ввести еще значение(0 или 1)? "))
	dump(globals()[name_mass], file)
	choise_mass = int(CheckValueForChoise(input("Создать еще массив(0 или 1)? "), "Создать еще массив(0 или 1)? "))
	if choise_mass:
		return FillingOutFile()
	else:
		return

name_file = CheckValue(input("Введите имя файла: "), "Введите имя файла: ") + ".dat"
names_mass = []

file = open(name_file, "wb")
FillingOutFile()
file.close()
