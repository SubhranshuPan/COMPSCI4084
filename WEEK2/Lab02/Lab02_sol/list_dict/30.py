info = {"p1": {"name": "Som", "age": 21, "shoe_size": 9},
        "p2": {"name": "Manas", "age": 23, "shoe_size": 8},
        "p3": {"name": "Ash", "age": 26, "shoe_size": 10},
        "p4": {"name": "Sky", "age": 25, "shoe_size": 9}
    }
for key in info:
    print(info[key]["name"] + ":", info[key]["age"])
remove_name = input("Enter name you want to remove: ")

for key in info:
    if info[key]["name"] == remove_name:
        info.pop(key)
        break
print("Name not in Data")

for key in info:
    print(info[key])
    