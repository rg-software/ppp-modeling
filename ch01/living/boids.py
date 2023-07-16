# TODO: **2 => x*x; get rid of sqrt
# check with python -m cProfile -s tottime boids.py

import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
MIN_V = 5
MAX_V = 20
MIN_DISTANCE = 40
AVOID_F = 0.09
VISUAL_RANGE = 200
CENTERING_F = 0.03
VMATCH_F = 0.02
VRETURN_F = 3.0
RET_MARGIN = 70
R = 10
MARGIN = 50
SLEEP_MS = 20
N = 100  # number of boids


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


def clamp(v, max_v):
    return math.copysign(min(abs(v), max_v), v)


@dataclass
class Boid:
    m: turtle.Turtle
    vx: float
    vy: float

    def distance(self, b):
        dx = b.m.xcor() - self.m.xcor()
        dy = b.m.ycor() - self.m.ycor()
        # return math.sqrt(dx * dx + dy * dy)  #
        return math.sqrt(dx**2 + dy**2)

    def neighbors(self, dist):
        return [b for b in boids if b != self and self.distance(b) < dist]

    def move(self):
        self.rule1()
        self.rule2()
        self.rule3()
        self.rule4()

        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)
        self.m.setheading(math.degrees(math.atan2(self.vy, self.vx)))

    # towards center of mass of neighbors
    def rule1(self):
        neighbors = self.neighbors(VISUAL_RANGE)

        if neighbors:
            cx = sum(b.m.xcor() for b in neighbors) / len(neighbors)
            cy = sum(b.m.ycor() for b in neighbors) / len(neighbors)

            self.vx += (cx - self.m.xcor()) * CENTERING_F
            self.vy += (cy - self.m.ycor()) * CENTERING_F

    # keep a small dist away from other objects
    def rule2(self):
        neighbors = self.neighbors(MIN_DISTANCE)

        if neighbors:
            mx = sum(self.m.xcor() - b.m.xcor() for b in neighbors)
            my = sum(self.m.ycor() - b.m.ycor() for b in neighbors)

            self.vx += mx * AVOID_F
            self.vy += my * AVOID_F

    # match velocity with neighbors
    def rule3(self):
        neighbors = self.neighbors(VISUAL_RANGE)

        if neighbors:
            px = sum(b.vx for b in neighbors) / len(neighbors)
            py = sum(b.vy for b in neighbors) / len(neighbors)

            self.vx += (px - self.vx) * VMATCH_F
            self.vy += (py - self.vy) * VMATCH_F

    def rule4(self):
        if abs(self.m.xcor()) > WIDTH / 2 - RET_MARGIN:
            self.vx -= math.copysign(VRETURN_F, self.m.xcor())
        if abs(self.m.ycor()) > HEIGHT / 2 - RET_MARGIN:
            self.vy -= math.copysign(VRETURN_F, self.m.ycor())

        if (v := math.sqrt(self.vx**2 + self.vy**2)) > MAX_V:
            self.vx = MAX_V * self.vx / v
            self.vy = MAX_V * self.vy / v

    @classmethod
    def create(cls):
        x = uniform(-WIDTH / 2 + R, WIDTH / 2 - R)
        y = uniform(-HEIGHT / 2 + R, HEIGHT / 2 - R)
        m = turtle.Turtle()
        m.penup()
        m.goto(x, y)
        v = uniform(MIN_V, MAX_V)
        angle = uniform(0, 2 * math.pi)
        return cls(m, v * math.cos(angle), v * math.sin(angle))


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


sim_state = SimState.setup()
setup_screen("Boids")
boids = [Boid.create() for _ in range(N)]


def tick():
    if not sim_state.done:
        for b in boids:
            b.move()

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
