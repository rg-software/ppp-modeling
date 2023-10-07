import turtle
import math

WIDTH = 600
HEIGHT = 400
MARGIN = 50
SLEEP_MS = 20
TURTLE_SIZE = 20

R_SUN = 60
R_EARTH = 20
L_EARTH = 130
AV_EARTH = 0.02
R_MOON = 3
L_MOON = 30
AV_MOON = AV_EARTH * 13

done = False


def set_done():
    global done
    done = True


def init_object(color, r, distance):
    m = turtle.Turtle()
    m.shape("circle")
    m.color(color)
    m.shapesize(2 * r / TURTLE_SIZE)
    m.penup()
    m.goto(distance, 0)
    return m


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Digital orrery")

turtle.listen()
turtle.onkeypress(set_done, "space")

sun = init_object("yellow", R_SUN, 0)
earth = init_object("blue", R_EARTH, L_EARTH)
moon = init_object("black", R_MOON, L_EARTH + L_MOON)

a_earth = a_moon = 0


def tick():
    if not done:
        global a_earth, a_moon

        earth.goto(L_EARTH * math.cos(a_earth), L_EARTH * math.sin(a_earth))
        moon.goto(
            earth.xcor() + L_MOON * math.cos(a_moon),
            earth.ycor() + L_MOON * math.sin(a_moon),
        )

        a_earth += AV_EARTH
        a_moon += AV_MOON

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
