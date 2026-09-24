import turtle
import random
turtle.shape("turtle")
num_lines = random.randint(10, 30)

for i in range(num_lines):
    length = random.randint(20, 150)
    angle = random.randint(1, 360)
    turtle.forward(length)
    turtle.right(angle)

turtle.exitonclick()
