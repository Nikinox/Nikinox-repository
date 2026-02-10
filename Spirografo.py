import turtle

turtle.speed(0)
turtle.bgcolor('black')

for i in range(5):
    for colour in ['red', 'magenta', 'yellow', 'blue', 'orange', 'green', 'white']:
        turtle.color(colour)
        turtle.pensize(3)
        turtle.left(12)

        # Disegno di un quadrato
        for _ in range(4):
            turtle.forward(200)
            turtle.left(90)
