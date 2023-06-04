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
        turtle.onkey(r.set_done, "space")
        return r


def setup_screen(title):
    turtle.Screen().setup(WIDTH + MARGIN, HEIGHT + MARGIN)
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


@dataclass
class Ball:
    m: turtle.Turtle
    vx: float
    vy: float
    r: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if abs(self.m.xcor()) > WIDTH / 2 - self.r:
            self.vx *= -1

        if abs(self.m.ycor()) > HEIGHT / 2 - self.r:
            self.vy *= -1

    def mass(self):
        return math.pi * (self.r ** 2)

    @classmethod
    def create(cls):
        size = uniform(MIN_SIZE_FACTOR, MAX_SIZE_FACTOR)
        r = size * R
        x = uniform(-WIDTH / 2 + r, WIDTH / 2 - r)
        y = uniform(-HEIGHT / 2 + r, HEIGHT / 2 - r)
        m = turtle.Turtle()
        m.shape("circle")
        m.shapesize(size)
        m.penup()
        m.goto(x, y)
        v = uniform(MIN_V, MAX_V)
        angle = uniform(0, 2 * math.pi)
        return Ball(m, v * math.cos(angle), v * math.sin(angle), r)


def balls_collide(b1, b2):
    d = math.sqrt((b1.m.xcor() - b2.m.xcor()) ** 2 + (b1.m.ycor() - b2.m.ycor()) ** 2)
    return d <= b1.r + b2.r


def process_collision(b1, b2):
    a = math.atan2(b2.m.ycor() - b1.m.ycor(), b2.m.xcor() - b1.m.xcor())
    A1n = math.atan2(b1.vy, b1.vx) - a
    A2n = math.atan2(b2.vy, b2.vx) - a

    v1 = math.sqrt(b1.vx ** 2 + b1.vy ** 2)
    v2 = math.sqrt(b2.vx ** 2 + b2.vy ** 2)

    vr1 = v1 * math.cos(A1n)
    vt1 = v1 * math.sin(A1n)

    vr2 = v2 * math.cos(A2n)
    vt2 = v2 * math.sin(A2n)

    m1, m2 = b1.mass(), b2.mass()
    vr1n = (vr1 * (m1 - m2) + 2 * m2 * vr2) / (m1 + m2)
    vr2n = vr1 + vr1n - vr2

    v1n = math.sqrt(vr1n ** 2 + vt1 ** 2)
    v2n = math.sqrt(vr2n ** 2 + vt2 ** 2)

    A1nn = math.atan2(vt1, vr1n) + a
    A2nn = math.atan2(vt2, vr2n) + a

    b1.vx = v1n * math.cos(A1nn)
    b1.vy = v1n * math.sin(A1nn)

    b2.vx = v2n * math.cos(A2nn)
    b2.vy = v2n * math.sin(A2nn)


sim_state = SimState.setup()
setup_screen("Free kick")
draw_vessel()

b1 = Ball.create()
b2 = Ball.create()


def tick():
    if not sim_state.done:
        b1.move()
        b2.move()

        if balls_collide(b1, b2):
            process_collision(b1, b2)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
