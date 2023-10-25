import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
V = 15
FORCE = 9
R = 10
MARGIN = 50
SLEEP_MS = 20
BULB = (0, 0)
BULB_RANGE = 70


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


@dataclass
class Moth:
    moth: turtle.Turtle
    v: tuple[float, float]

    @classmethod
    def create(cls):
        moth = turtle.Turtle()
        moth.penup()
        moth.setx(uniform(-WIDTH / 2 + R, WIDTH / 2 - R))
        moth.sety(uniform(-HEIGHT / 2 + R, HEIGHT / 2 - R))

        angle = uniform(0, 2 * math.pi)
        v = (V * math.cos(angle), V * math.sin(angle))

        return cls(moth, v)

    def move(self):
        bulb_direction = vecdiff(BULB, (self.moth.xcor(), self.moth.ycor()))

        if length(bulb_direction) < BULB_RANGE:
            bulb_direction = (-bulb_direction[0], -bulb_direction[1])

        v_desired = scale(bulb_direction, V)
        steering = vecdiff(v_desired, self.v)
        acceleration = scale(steering, FORCE)
        self.v = scale(vecsum(self.v, acceleration), V)

        x_new, y_new = self.moth.xcor() + self.v[0], self.moth.ycor() + self.v[1]
        self.moth.setheading(self.moth.towards(x_new, y_new))
        self.moth.goto(x_new, y_new)


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


sim_state = SimState.setup()
setup_screen("Dancing moth")

bulb = turtle.Turtle()
bulb.shape("circle")

N = 20
moth = [Moth.create() for _ in range(N)]


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
        for m in moth:
            m.move()

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
