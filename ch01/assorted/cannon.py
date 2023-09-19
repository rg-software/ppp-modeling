import turtle
import math
from random import uniform

WIDTH = 600
HEIGHT = 400
V = 4
# LOSS_COEFF = 0.8
R = 10
REARTH = 100
MARGIN = 50
ACCEL = -0.1

done = False
right_wall = WIDTH / 2 - R
bottom_wall = -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Cannon")

turtle.listen()
turtle.onkeypress(set_done, "space")

e = turtle.Turtle()
e.shape("circle")
e.shapesize(2 * REARTH / 20)

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

m.goto(0, +REARTH + R + 14)
# m.goto(-right_wall, 0)
# uniform(-right_wall, right_wall), uniform(-top_wall, top_wall))

# angle = uniform(0, 2 * math.pi)
vx = V  # * math.cos(angle)
vy = 0  # V * math.sin(angle)


def mult(vec, factor):
    return (vec[0] * factor, vec[1] * factor)


def length(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def scale(vec, new_len):
    return mult(vec, new_len / length(vec))


def vecsum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def tick():
    if not done:
        global vx, vy
        m.goto(m.xcor() + vx, m.ycor() + vy)

        if length((m.xcor(), m.ycor())) < REARTH + R:
            set_done()
        # if m.xcor() > right_wall:
        #     vx *= -1
        #     set_done()

        # if m.ycor() < bottom_wall:
        #     m.goto(m.xcor(), bottom_wall)
        #     vy *= -LOSS_COEFF

        # vy += acceleration

        av = (m.xcor(), m.ycor())
        av = scale(av, ACCEL)
        vx, vy = vecsum((vx, vy), av)

        turtle.update()
        turtle.ontimer(tick, 20)


tick()
turtle.done()
