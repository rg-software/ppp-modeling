import turtle
import math
from random import uniform

WIDTH = 600
HEIGHT = 400
V = 2
LOSS_COEFF = 0.8
R = 10
MARGIN = 50

done = False
right_wall = WIDTH / 2 - R
bottom_wall = -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Falling ball")

turtle.listen()
turtle.onkeypress(set_done, "space")

m = turtle.Turtle()
m.shape("circle")
m.penup()

# let's draw a vessel
m.goto(-WIDTH / 2, -HEIGHT / 2)
m.pendown()
m.sety(HEIGHT / 2)
m.setx(WIDTH / 2)
m.sety(-HEIGHT / 2)
m.setx(-WIDTH / 2)
m.penup()

m.goto(-right_wall, 0)
# uniform(-right_wall, right_wall), uniform(-top_wall, top_wall))

# angle = uniform(0, 2 * math.pi)
vx = V  # * math.cos(angle)
vy = 0  # V * math.sin(angle)
acceleration = -0.3


def tick():
    if not done:
        global vx, vy
        m.goto(m.xcor() + vx, m.ycor() + vy)

        if m.xcor() > right_wall:
            set_done()

        if m.ycor() < bottom_wall:
            m.goto(m.xcor(), bottom_wall)
            vy *= -LOSS_COEFF

        vy += acceleration

        turtle.update()
        turtle.ontimer(tick, 20)


tick()
turtle.done()
