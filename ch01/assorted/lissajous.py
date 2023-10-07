import turtle

WIDTH = 600
HEIGHT = 400
MARGIN = 50
SLEEP_MS = 20

AX_COEFF = -0.003
AY_COEFF = -0.001
START_COORDS = (100, 200)

done = False


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Lissajous figures")

turtle.listen()
turtle.onkeypress(set_done, "space")

m = turtle.Turtle()
m.shape("circle")
m.penup()
m.goto(START_COORDS[0], START_COORDS[1])
m.pendown()

vx, vy = 0, 0


def tick():
    if not done:
        global vx, vy

        m.goto(m.xcor() + vx, m.ycor() + vy)

        vx += m.xcor() * AX_COEFF
        vy += m.ycor() * AY_COEFF

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
