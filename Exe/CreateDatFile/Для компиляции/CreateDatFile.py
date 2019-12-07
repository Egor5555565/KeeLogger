from pickle import dump
data = []
your_email = input("Введите почту отпрвителя: ")
data.append(your_email)
your_password = input("Введите пароль отпрвителя: ")
data.append(your_password)
recipient_email = input("Введите почту получателя: ")
data.append(recipient_email)
f = open("data.dat", "wb")
dump(data, f)
f.close()
