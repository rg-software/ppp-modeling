import turtle
import math

WIDTH = 600
HEIGHT = 400
MARGIN = 50
SLEEP_MS = 20

# astroid
# R_FRAME = 25 * 4
# R_COG = 25
# R_PEN = 25

R_FRAME = 154
R_COG = 55
R_PEN = 30

L = R_FRAME - R_COG
AV = 0.1

done = False


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Spirograph curves")

turtle.listen()
turtle.onkeypress(set_done, "space")

pen = turtle.Turtle()
pen.shape("circle")
pen.penup()
pen.goto(L + R_PEN, 0)
pen.pendown()

a = 0


def tick():
    if not done:
        global a

        A = -a * R_COG / L
        x = L * math.cos(A)
        y = L * math.sin(A)
        pen.goto(x + R_PEN * math.cos(a), y + R_PEN * math.sin(a))

        a += AV

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
