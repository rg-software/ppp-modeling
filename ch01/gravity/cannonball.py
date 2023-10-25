import turtle
import math

WIDTH = 600
HEIGHT = 400
V = 3.2
R = 5
R_EARTH = 100
PEDESTAL_H = 14
ACCELERATION = -1000
MARGIN = 50
TURTLE_SIZE = 20
SLEEP_MS = 20

done = False
right_wall = WIDTH / 2 - R
bottom_wall = -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Newton's cannonball")

turtle.listen()
turtle.onkeypress(set_done, "space")

# draw the planet
earth = turtle.Turtle()
earth.shape("circle")
earth.color("blue")
earth.shapesize(2 * R_EARTH / TURTLE_SIZE)

m = turtle.Turtle()
m.shape("circle")
m.shapesize(2 * R / TURTLE_SIZE)
m.goto(0, R + R_EARTH + PEDESTAL_H)

vx = V
vy = 0


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

        r = length((m.xcor(), m.ycor()))

        if r < R_EARTH + R:
            set_done()

        a = scale((m.xcor(), m.ycor()), ACCELERATION / (r**2))
        vx, vy = vecsum((vx, vy), a)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
