import sqlite3

with sqlite3.connect("PhoneBook1.db") as db:
    cursor = db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS Names(
            ID INTEGER PRIMARY KEY,
            FIRSTNAME TEXT,
            SURNAME TEXT,
            PHONENUMBER TEXT); """)

cursor.execute(""" INSERT INTO Names(ID, FIRSTNAME, SURNAME, PHONENUMBER)
VALUES(1, 'Simon', 'Pierre', '0142678 9056') """)
db.commit()

cursor.execute(""" INSERT INTO Names(ID, FIRSTNAME, SURNAME, PHONENUMBER)
VALUES(2, 'Katarina', 'Iglesias', '0203456 7078') """)
db.commit()

cursor.execute(""" INSERT INTO Names(ID, FIRSTNAME, SURNAME, PHONENUMBER)
VALUES(3, 'Derrick', 'Brown', '0122345 8765') """)
db.commit()

cursor.execute(""" INSERT INTO Names(ID, FIRSTNAME, SURNAME, PHONENUMBER)
VALUES(4, 'John', 'Smith', '0112653 2312') """)
db.commit()

cursor.execute(""" INSERT INTO Names(ID, FIRSTNAME, SURNAME, PHONENUMBER)
VALUES(5, 'Mark', 'Isaac', '0141657 1383') """)
db.commit()

# cursor.execute("SELECT * FROM Names")
# for row in cursor.fetchall():
#     print(row)

print("Main Menu")
print("1) View phone book")
print("2) Add to phone book")
print("3) Search for surname")
print("4) Delete person from phone book")
print("5) Quit programme")

choice = int(input("Enter a number of your choice: "))

while choice != 5:
    if choice == 1:
        cursor.execute("SELECT * FROM Names")
        for row in cursor.fetchall():
            print(row)
    
    elif choice == 2:
        print("Adding record to database , enter the required details!")
        firstname = input("Enter first name: ")
        surname = input("Enter surname: ")
        phone = input("Enter phone number: ")

        cursor.execute(""" INSERT INTO Names(FIRSTNAME, SURNAME, PHONENUMBER)
        VALUES (?, ?, ?)""", (firstname, surname, phone))
        db.commit()
        print("Record added.")

    elif choice == 3:
        lastname = input("Enter surname to search for: ")
        cursor.execute("SELECT * FROM Names WHERE SURNAME = ?", (lastname,))
        for row in cursor.fetchall():
            print(row)

    elif choice == 4:
        id = int(input("Enter id of person to delete: "))
        cursor.execute("DELETE FROM Names WHERE ID = ?", (id,))
        db.commit()
        print("Record Deleted.")

    else:
        print("Enter a vallid choice.")

    print("Main Menu")
    print("1) View phone book")
    print("2) Add to phone book")
    print("3) Search for surname")
    print("4) Delete person from phone book")
    print("5) Quit programme")

    choice = int(input("Enter a number of your choice: "))

db.close()