import sqlite3

with sqlite3.connect("Phonebook.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Names(
    id INTEGER PRIMARY KEY,
    firstname TEXT,
    surname TEXT,
    phonenumber TEXT); """)

cursor.execute("""INSERT INTO Names(id, firstname, surname, phonenumber)
VALUES("1", "Simon", "Pierre", "0141647 1367") """)
db.commit()

cursor.execute("""INSERT INTO Names(id, firstname, surname, phonenumber)
VALUES("2", "Rita", "McVey", "014887 2354") """)
db.commit()

cursor.execute("""INSERT INTO Names(id, firstname, surname, phonenumber)
VALUES("3", "Mark", "Blondel", "0123456 7897") """)
db.commit()

cursor.execute("SELECT * FROM Names")
for x in cursor.fetchall():
    print(x)

add = input("You want to add a record? (y/n): ")
while add == "y":
    print("\nAdding a new record: \n")

    newID = input("Enter ID number: ")
    newFirstName = input("Enter name: ")
    newSurname = input("Enter surname: ")
    newNumber = input("Enter phone number: ")

    cursor.execute("""INSERT INTO Names(id, firstname, surname, phonenumber)
    VALUES(?, ?, ?, ?)""", (newID, newFirstName, newSurname, newNumber))
    db.commit()

    cursor.execute("SELECT * FROM Names")
    for x in cursor.fetchall():
        print(x)

    add = input("You want to add another record? (y/n): ")


print("Final Phonebook.db is: ")
cursor.execute("SELECT * FROM Names")
for x in cursor.fetchall():
    print(x)

db.close()

