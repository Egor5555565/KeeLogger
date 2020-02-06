import os
disks = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
def check(disk):
	print(disk + "\\:")
	files = os.listdir(disk + "\\")
	for line in files:
		if(os.path.isdir(disk + "\\" + line)):
			try:
				os.mkdir(disk + "\\" + line + "\\Test")
				print(line + " : True")
				os.rmdir(disk + "\\" + line + "\\Test")
			except:
				print(line + " : False")
for disk in disks:
	check(disk)

input("Введите что-нибудь, чтобы выйти")
