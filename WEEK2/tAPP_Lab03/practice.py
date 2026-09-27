# import sys

# if len(sys.argv) != 2:
#     print("A file name must be provided as a command line", \
#         "argument.")
#     quit()

# inf = open(sys.agrv[1], "r")

# total = 0

# line = inf.readline()

# while line != "":
#     total = total + float(line)
#     line = inf.readline()

# inf.close()
# print("The total of values in", sys.argv[1], "is", total)

fname = input("Enter file name: ")
file_opened = False

while file_opened == False:
    try:
        inf = open(fname, "r")
        file_opened = True
    except FileNotFoundError:
        print("'%s' could not be opned, Quitting...")
        fname = input("Enter the file name: ")

    