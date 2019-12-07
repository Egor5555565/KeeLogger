import pickle

name_file = input("Введите название файла(без расширения): ")
common = []
def read():
	try:
		common.append(pickle.load(file))
		return read()
	except:
		return

file = open( name_file + ".dat", "rb")
read()
file.close()

for mass in common: print(mass)

input("Введите что-нибудь для выхода...")