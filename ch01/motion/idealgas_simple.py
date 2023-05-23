import turtle
import time
import math
import random
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
VELOCITY = 5
R = 10
MARGIN = 50
N = 20

done = False

left_wall, right_wall = -WIDTH / 2 + R, WIDTH / 2 - R
top_wall, bottom_wall = HEIGHT / 2 - R, -HEIGHT / 2 + R


def set_done():
    global done
    done = True


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


turtle.Screen().setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Ideal gas (simple version)")
turtle.listen()
turtle.onkey(set_done, "space")


@dataclass
class Molecule:
    m: turtle.Turtle
    vx: float
    vy: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if not left_wall < self.m.xcor() < right_wall:
            self.vx *= -1

        if not bottom_wall < self.m.ycor() < top_wall:
            self.vy *= -1


def make_molecule():
    m = turtle.Turtle()
    m.shape("circle")
    m.penup()
    m.goto(random.uniform(left_wall, right_wall), random.uniform(bottom_wall, top_wall))

    angle = random.uniform(0, 2 * math.pi)
    return Molecule(m, VELOCITY * math.cos(angle), VELOCITY * math.sin(angle))


draw_vessel()
molecules = [make_molecule() for _ in range(N)]

while not done:
    for m in molecules:
        m.move()

    turtle.update()
    time.sleep(0.01)

turtle.done()
