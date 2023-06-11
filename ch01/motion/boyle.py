import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
V = 10
R = 10
MARGIN = 50
SLEEP_MS = 20
N = 20  # number of molecules in our vessel

left_wall, right_wall = -WIDTH / 2 + R, WIDTH / 2 - R
top_wall, bottom_wall = HEIGHT / 2 - R, -HEIGHT / 2 + R


@dataclass
class SimState:
    done: bool
    delta_p: float
    delta_t: int

    def set_done(self):
        self.done = True

    def pressure(self):
        area = 2 * (top_wall - bottom_wall + right_wall - left_wall)
        force = self.delta_p / self.delta_t
        return force / area

    @classmethod
    def setup(cls):
        r = cls(False, 0, 0)
        turtle.listen()
        turtle.onkey(r.set_done, "space")
        return r


@dataclass
class Molecule:
    m: turtle.Turtle
    vx: float
    vy: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if not left_wall < self.m.xcor() < right_wall:
            self.vx *= -1
            sim_state.delta_p += abs(self.vx)

        if not bottom_wall < self.m.ycor() < top_wall:
            self.vy *= -1
            sim_state.delta_p += abs(self.vy)

    @classmethod
    def create(cls):
        m = turtle.Turtle()
        m.shape("circle")
        m.penup()
        m.goto(uniform(left_wall, right_wall), uniform(bottom_wall, top_wall))

        angle = uniform(0, 2 * math.pi)
        return cls(m, V * math.cos(angle), V * math.sin(angle))


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
setup_screen("Boyle-Mariotte's law")
draw_vessel()
molecules = [Molecule.create() for _ in range(N)]


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()

        sim_state.delta_t += 1

        if sim_state.delta_t % 100 == 0:
            vol = (top_wall - bottom_wall) * (right_wall - left_wall)
            print(sim_state.pressure() * vol)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
