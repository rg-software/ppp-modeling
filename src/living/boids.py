import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
MARGIN = 50
R = 10
SLEEP_MS = 20
MIN_V = 5
MAX_V = 20
MIN_DISTANCE = 20
AVOID_F = 0.09
VISUAL_RANGE = 200
CENTERING_F = 0.03
VMATCH_F = 0.04
VRETURN_F = 3.0
RET_MARGIN = 70
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


def mult(vec, factor):
    return (vec[0] * factor, vec[1] * factor)


def length(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])


def scale(vec, new_len):
    return mult(vec, new_len / length(vec))


def vecsum(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def vecdiff(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])


@dataclass
class Boid:
    m: turtle.Turtle
    v: tuple

    def distance_sq(self, b):
        dx = b.m.xcor() - self.m.xcor()
        dy = b.m.ycor() - self.m.ycor()
        return dx * dx + dy * dy

    def neighbors(self, dist):
        dist_sq = dist * dist
        return [b for b in boids if b != self and self.distance_sq(b) < dist_sq]

    def move(self):
        self.rule_separation()
        self.rule_alignment()
        self.rule_cohesion()
        self.rule_limits()

        x_new, y_new = self.m.xcor() + self.v[0], self.m.ycor() + self.v[1]
        self.m.setheading(self.m.towards(x_new, y_new))
        self.m.goto(x_new, y_new)

    # towards center of mass of neighbors
    def rule_cohesion(self):
        neighbors = self.neighbors(VISUAL_RANGE)

        if neighbors:
            cx = sum(b.m.xcor() for b in neighbors) / len(neighbors)
            cy = sum(b.m.ycor() for b in neighbors) / len(neighbors)
            center = (cx, cy)

            c_direction = vecdiff(center, (self.m.xcor(), self.m.ycor()))
            self.v = vecsum(self.v, mult(c_direction, CENTERING_F))

    # keep a small dist away from other objects
    def rule_separation(self):
        neighbors = self.neighbors(MIN_DISTANCE)

        if neighbors:
            vx = sum(self.m.xcor() - b.m.xcor() for b in neighbors)
            vy = sum(self.m.ycor() - b.m.ycor() for b in neighbors)
            target_v = (vx, vy)

            self.v = vecsum(self.v, mult(target_v, AVOID_F))

    # match velocity with neighbors
    def rule_alignment(self):
        neighbors = self.neighbors(VISUAL_RANGE)

        if neighbors:
            vx = sum(b.v[0] for b in neighbors) / len(neighbors)
            vy = sum(b.v[1] for b in neighbors) / len(neighbors)
            flock_v = (vx, vy)
            v_diff = vecdiff(flock_v, self.v)

            self.v = vecsum(self.v, mult(v_diff, VMATCH_F))

    # limit boid speed to MAX_V and steer away from the screen borders
    def rule_limits(self):
        ax, ay = 0, 0

        if abs(self.m.xcor()) > WIDTH / 2 - RET_MARGIN:
            ax = -math.copysign(VRETURN_F, self.m.xcor())
        if abs(self.m.ycor()) > HEIGHT / 2 - RET_MARGIN:
            ay = -math.copysign(VRETURN_F, self.m.ycor())

        self.v = vecsum(self.v, (ax, ay))
        if length(self.v) > MAX_V:
            self.v = scale(self.v, MAX_V)

    @classmethod
    def create(cls):
        x = uniform(-WIDTH / 2 + R, WIDTH / 2 - R)
        y = uniform(-HEIGHT / 2 + R, HEIGHT / 2 - R)
        m = turtle.Turtle()
        m.penup()
        m.goto(x, y)
        v = uniform(MIN_V, MAX_V)
        angle = uniform(0, 2 * math.pi)
        return cls(m, (v * math.cos(angle), v * math.sin(angle)))


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
