#upload data from csv file
import psycopg2

conn = psycopg2.connect(
	database="people",
	user="postgres",
	password="rootroot",
	host="localhost"
)
cursor = conn.cursor()
conn.autocommit = True
# CSV to TABLE

f = open("persons.csv", "r")
cursor.copy_from(f, 'phonebook', sep=',')
f.close()

def update():
	first = input("Enter firstname: " )
	last = input("Enter lastname: ")
	phone_number = input("Enter your new number: ")
	sql = f"update PhoneBook set phone_num = {phone_number} where first_name = \'{first}\' and last_name = \'{last}\'"
	cursor.execute(sql)
	print("RECORD IS UPDATED SUCCESSFULLY!")


def insert():
	print("ADDING NEW RECORD TO THE PHONEBOOK...")
	first = input("Enter firstname: ")
	last = input("Enter lastname: ")
	num = input("Enter your phone number: ")
	sql = f"insert into PhoneBook values (%s, %s, %s)"
	insert_data = (first, last, num)
	cursor.execute(sql, insert_data)
	print("RECORD IS ADDED SUCCESSFULLY!")

def delete():
	print("DELETING RECORD FROM THE PHONEBOOK...")
	first = input("Enter firstname: ")
	last = input("Enter lastname: ")
	sql = f"delete from PhoneBook where first_name = \'{first}\' and last_name = \'{last}\'"
	cursor.execute(sql)
	print("RECORD IS DELETED SUCCESSFULLY!")

def filter_by_first_name(first_name):
	sql = f"select * from PhoneBook where first_name = \'{first_name}\'"
	cursor.execute(sql)
	result = cursor.fetchall()
	if len(result) > 0:
		for i, value in enumerate(result):
			print(f"{i+1}) ",value[0], value[1], value[2])
	else:
		print("RECORDS NOT FOUND")

def filter_by_phone(phone_number):
	sql = f"select * from PhoneBook where phone_num = \'{phone_number}\'"
	cursor.execute(sql)
	result = cursor.fetchall()
	if len(result) > 0:
		for i, value in enumerate(result):
			print(f"{i+1}) ",value[0], value[1], value[2])
	else:
		print("RECORDS NOT FOUND")

def filter_by_surname(last_name):
	sql = f"select * from PhoneBook where last_name = \'{last_name}\'"
	cursor.execute(sql)
	result = cursor.fetchall()
	if len(result) > 0:
		for i, value in enumerate(result):
			print(f"{i+1}) ",value[0], value[1], value[2])
	else:
		print("RECORDS NOT FOUND")

def filter_by_name_and_surname(first_name, last_name):
	sql = f"select * from PhoneBook where first_name = \'{first_name}\' and last_name = \'{last_name}\'"
	cursor.execute(sql)
	result = cursor.fetchall()
	if len(result) > 0:
		for i, value in enumerate(result):
			print(f"{i+1}) ",value[0], value[1], value[2])
	else:
		print("RECORDS NOT FOUND")
	

def start():
	command = input("Select command: \n[1] - INSERT\n[2] - UPDATE\n[3] - DELETE\n[4] - RETRIEVE\n")
	if command == "1":
		insert()
	elif command == "2":
		update()
	elif command == "3":
		delete()
	elif command == "4":
		subcommand = input("Select command: \n[1] - SEARCH BY NAME\n[2] - SEARCH BY SURNAME\n[3] - SEARCH BY PHONE\n[4] - SEARCH BY NAME AND SURNAME\n")
		if subcommand == "1":
			name = input("Enter firstname: " )
			filter_by_first_name(name)
		elif subcommand == "2":
			surname = input("Enter surname: " )
			filter_by_surname(surname)
		elif subcommand == "3":
			phone = input("Phone: ")
			filter_by_phone(phone)
		elif subcommand == "4":
			firstname = input("Enter name: ")
			lastname = input("Enter lastname: ")
			filter_by_name_and_surname(first_name=firstname, last_name=lastname)
	else:
		print("INVALID COMMAND")	



start()







conn.commit()
conn.close()