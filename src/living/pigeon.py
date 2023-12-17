import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
V = 10
VMAX = V
VMIN = 3
FORCE = 2
R = 10
MARGIN = 50
SLEEP_MS = 20
NEST = (0, 0)
NEST_RANGE = 70


@dataclass
class SimState:
    done: bool

    def set_done(self):
        self.done = True

    @classmethod
    def setup(cls):
        r = cls(False)
        turtle.listen()
        turtle.onkeypress(r.set_done, "space")
        return r


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


sim_state = SimState.setup()
setup_screen("Homing pigeon")

bulb = turtle.Turtle()
bulb.shape("circle")
bulb.color("green")

pigeon = turtle.Turtle()
pigeon.penup()
pigeon.setx(uniform(-WIDTH / 2 + R, WIDTH / 2 - R))
pigeon.sety(uniform(-HEIGHT / 2 + R, HEIGHT / 2 - R))

angle = uniform(0, 2 * math.pi)
v = (V * math.cos(angle), V * math.sin(angle))


def mult(vec, factor):
    return (vec[0] * factor, vec[1] * factor)


def length(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def scale(vec, new_len):
    return mult(vec, new_len / length(vec))


def vecsum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def vecdiff(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])


def tick():
    if not sim_state.done:
        global v, V

        bulb_direction = vecdiff(NEST, (pigeon.xcor(), pigeon.ycor()))

        v_desired = scale(bulb_direction, V)
        steering = vecdiff(v_desired, v)
        acceleration = scale(steering, FORCE)
        v = scale(vecsum(v, acceleration), V)

        x_new, y_new = pigeon.xcor() + v[0], pigeon.ycor() + v[1]

        if V > VMIN:
            pigeon.setheading(pigeon.towards(x_new, y_new))
        pigeon.goto(x_new, y_new)

        V = min(VMAX * length(bulb_direction) / NEST_RANGE, VMAX)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
