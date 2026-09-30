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

cursor.execute("SELECT * FROM Names")
for row in cursor.fetchall():
    print(row)

db.close()