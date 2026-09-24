import turtle
import random
turtle.shape("turtle")
colors = ["red", "blue", "green", "orange", "purple", "black"]

for i in range(8):
    turtle.pencolor(random.choice(colors))
    turtle.forward(100)
    turtle.right(45)

turtle.exitonclick()