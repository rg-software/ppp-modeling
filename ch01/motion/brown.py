import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
MIN_V = 5
MAX_V = 15
R = 10
PARTICLE_SIZE_FACTOR = 7
MARGIN = 50
SLEEP_MS = 20
N = 30  # number of molecules in our vessel

left_wall, right_wall = -WIDTH / 2 + R, WIDTH / 2 - R
top_wall, bottom_wall = HEIGHT / 2 - R, -HEIGHT / 2 + R


@dataclass
class SimState:
    done: bool
    prev_collisions: set

    def set_done(self):
        self.done = True

    @classmethod
    def setup(cls):
        r = cls(False, set())
        turtle.listen()
        turtle.onkey(r.set_done, "space")
        return r


def clamp(v, min_v, max_v):
    return min(max(min_v, v), max_v)


@dataclass
class Molecule:
    m: turtle.Turtle
    vx: float
    vy: float
    r: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if abs(self.m.xcor()) >= WIDTH / 2 - self.r:
            self.vx *= -1

        if abs(self.m.ycor()) >= HEIGHT / 2 - self.r:
            self.vy *= -1

        right_wall = WIDTH / 2 - self.r - 1
        top_wall = HEIGHT / 2 - self.r - 1

        self.m.setx(clamp(self.m.xcor(), -right_wall, right_wall))
        self.m.sety(clamp(self.m.ycor(), -top_wall, top_wall))

    def mass(self):
        return math.pi * (self.r ** 2)

    @classmethod
    def create(cls, size):
        r = size * R
        m = turtle.Turtle()
        m.shape("circle")
        m.shapesize(size)
        m.penup()
        m.goto(uniform(left_wall, right_wall), uniform(bottom_wall, top_wall))

        angle = uniform(0, 2 * math.pi)
        v = uniform(MIN_V, MAX_V)
        return cls(m, v * math.cos(angle), v * math.sin(angle), r)


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
    # m1 = m2 = math.pi * (R ** 2)

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


sim_state = SimState.setup()
setup_screen("Brownian motion")
draw_vessel()
molecules = [Molecule.create(1) for _ in range(N)]
particle = Molecule.create(PARTICLE_SIZE_FACTOR)
particle.vx = particle.vy = 0
particle.m.goto(0, 0)
molecules.append(particle)


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()

        collisions = set()
        for i in range(len(molecules)):
            for j in range(0, i):
                if balls_collide(molecules[i], molecules[j]):
                    collisions.add((i, j))
                    if not (i, j) in sim_state.prev_collisions:
                        process_collision(molecules[i], molecules[j])

        sim_state.prev_collisions = collisions

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
