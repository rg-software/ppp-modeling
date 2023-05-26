import turtle
import math
from random import uniform

WIDTH = 600
HEIGHT = 400
VELOCITY = 10
R = 10
MARGIN = 50

done = False

left_wall, right_wall = -WIDTH / 2 + R, WIDTH / 2 - R
top_wall, bottom_wall = HEIGHT / 2 - R, -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.Screen().setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("A molecule of gas")
turtle.listen()
turtle.onkey(set_done, "space")

m = turtle.Turtle()
m.shape("circle")
m.penup()

# let's draw a vessel
m.goto(-WIDTH / 2, -HEIGHT / 2)
m.pendown()
m.sety(HEIGHT / 2)
m.setx(WIDTH / 2)
m.sety(-HEIGHT / 2)
m.setx(-WIDTH / 2)
m.penup()

m.goto(uniform(left_wall, right_wall), uniform(bottom_wall, top_wall))

angle = uniform(0, 2 * math.pi)
vx = VELOCITY * math.cos(angle)
vy = VELOCITY * math.sin(angle)


def tick():
    if not done:
        global vx, vy
        m.goto(m.xcor() + vx, m.ycor() + vy)

        if not left_wall < m.xcor() < right_wall:
            vx *= -1

        if not bottom_wall < m.ycor() < top_wall:
            vy *= -1

        turtle.update()
        turtle.ontimer(tick, 20)


tick()
turtle.done()
