import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
MIN_V = 5
MAX_V = 15
MIN_SIZE_FACTOR = 0.7
MAX_SIZE_FACTOR = 4
START_DISTANCE = 400
R = 10
MARGIN = 50
SLEEP_MS = 20


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
class Ball:
    m: turtle.Turtle
    vx: float
    r: float

    def move(self):
        self.m.setx(self.m.xcor() + self.vx)

        if abs(self.m.xcor()) >= WIDTH / 2 - self.r:
            self.vx *= -1

    def mass(self):
        return math.pi * (self.r**2)

    @classmethod
    def create(cls, x, v_factor):
        size = uniform(MIN_SIZE_FACTOR, MAX_SIZE_FACTOR)
        r = size * R
        m = turtle.Turtle()
        m.shape("circle")
        m.shapesize(size)
        m.penup()
        m.goto(x, 0)

        return Ball(m, v_factor * uniform(MIN_V, MAX_V), r)


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


def draw_vessel():
    m = turtle.Turtle()
    m.hideturtle()
    m.penup()
    m.goto(-WIDTH / 2, -HEIGHT / 2)
    m.pendown()
    m.sety(HEIGHT / 2)
    m.setx(WIDTH / 2)
    m.sety(-HEIGHT / 2)
    m.setx(-WIDTH / 2)


def balls_collide(b1, b2):
    return abs(b1.m.xcor() - b2.m.xcor()) <= b1.r + b2.r


def process_collision(b1, b2):
    m1, m2 = b1.mass(), b2.mass()
    v1n = (b1.vx * (m1 - m2) + 2 * m2 * b2.vx) / (m1 + m2)
    v2n = b1.vx + v1n - b2.vx

    b1.vx = v1n
    b2.vx = v2n


sim_state = SimState.setup()
setup_screen("Central collision")
draw_vessel()

ball1 = Ball.create(-START_DISTANCE / 2, 1)
ball2 = Ball.create(START_DISTANCE / 2, -1)


def tick():
    if not sim_state.done:
        ball1.move()
        ball2.move()

        if balls_collide(ball1, ball2):
            process_collision(ball1, ball2)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
