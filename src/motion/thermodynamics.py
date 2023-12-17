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

right_wall = WIDTH / 2 - R
top_wall = HEIGHT / 2 - R


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
class Molecule:
    m: turtle.Turtle
    v: float
    vx: float
    vy: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if abs(self.m.xcor()) > right_wall:
            self.vx *= -1

        if abs(self.m.ycor()) > top_wall:
            self.vy *= -1

        near_hole = abs(self.m.ycor()) <= R_HOLE - R
        moves_right = -R < self.m.xcor() < 0 and self.vx > 0
        moves_left = 0 < self.m.xcor() < R and self.vx < 0

        if not near_hole and (moves_left or moves_right):
            self.vx *= -1

    @classmethod
    def create(cls, v, left, right, color):
        m = turtle.Turtle()
        m.shape("circle")
        m.color(color)
        m.penup()
        m.goto(uniform(left, right), uniform(-top_wall, top_wall))

        angle = uniform(0, 2 * math.pi)
        return cls(m, v, v * math.cos(angle), v * math.sin(angle))


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
molecules = [Molecule.create(V_COLD, -right_wall, -R, "blue") for _ in range(N)]
molecules.extend([Molecule.create(V_HOT, R, right_wall, "red") for _ in range(N)])

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()


def temperature(gas):
    return sum(mol.v**2 for mol in gas) / len(gas)


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()

        m_left = [mol for mol in molecules if mol.m.xcor() < 0]
        m_right = [mol for mol in molecules if mol.m.xcor() > 0]

        writer.clear()
        writer.goto(-100, HEIGHT / 2)
        writer.write(round(temperature(m_left)))
        writer.goto(100, HEIGHT / 2)
        writer.write(round(temperature(m_right)))

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
