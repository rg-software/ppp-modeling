import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
V_COLD = 5
V_HOT = 15
R_HOLE = 30
R = 10
MARGIN = 50
SLEEP_MS = 20
N = 20  # number of molecules in our vessel

left_wall, right_wall = -WIDTH / 2 + R, WIDTH / 2 - R
top_wall, bottom_wall = HEIGHT / 2 - R, -HEIGHT / 2 + R


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


@dataclass
class Molecule:
    m: turtle.Turtle
    v: float
    vx: float
    vy: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if not left_wall < self.m.xcor() < right_wall:
            self.vx *= -1

        if not bottom_wall < self.m.ycor() < top_wall:
            self.vy *= -1

        near_hole = -R_HOLE + R < self.m.ycor() < R_HOLE - R
        flies_right = -R < self.m.xcor() < 0 and self.vx > 0
        flies_left = 0 < self.m.xcor() < R and self.vx < 0

        if not near_hole and (flies_left or flies_right):
            self.vx *= -1

    @classmethod
    def create(cls, v, left, right, color):
        m = turtle.Turtle()
        m.shape("circle")
        m.color(color)
        m.penup()
        m.goto(uniform(left, right), uniform(bottom_wall, top_wall))

        angle = uniform(0, 2 * math.pi)
        return cls(m, v, v * math.cos(angle), v * math.sin(angle))


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
    m.penup()
    m.goto(0, -HEIGHT / 2)
    m.pendown()
    m.sety(-R_HOLE)
    m.penup()
    m.sety(R_HOLE)
    m.pendown()
    m.sety(HEIGHT / 2)


sim_state = SimState.setup()
setup_screen("Thermodynamics")
draw_vessel()
molecules = [Molecule.create(V_COLD, left_wall, -R, "blue") for _ in range(N)]
molecules.extend([Molecule.create(V_HOT, R, right_wall, "red") for _ in range(N)])

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()


def temperature(gas):
    return round(sum([mol.v for mol in gas]) / len(gas), 2)


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()

        m_left = [mol for mol in molecules if mol.m.xcor() < 0]
        m_right = [mol for mol in molecules if mol.m.xcor() > 0]

        writer.clear()
        writer.goto(-100, HEIGHT / 2)
        writer.write(temperature(m_left))
        writer.goto(100, HEIGHT / 2)
        writer.write(temperature(m_right))

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
