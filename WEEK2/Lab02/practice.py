# Repeition 

# Nested Loops
# Read the first message from the user
message = input("Enter a message (blank to quit): ")

# loop until the message is a blank line
while message != "":
    # read the number of times the message should be displayed
    n = int(input("How many times should it be repeated? "))

    # Display the message n times
    for i in range(n):
        print(message)

    message = input("Enter a message (blank to quit): ")


# Functions:
def drawbox(width, height, outline="*", fill=" "):
    if width < 4 or height < 4:
        print("Box is too small")
        quit()

    # Draw top of box
    print(outline * width)

    # Draw height if box
    for i in range(height - 4):
        print(outline + fill * (width - 4) + outline)

    # Draw bottom of box
    print(outline * width)


drawbox(24, 10, "&", ".")