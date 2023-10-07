import turtle

WIDTH = 600
HEIGHT = 400
V = 3
MINV = 0.01
LOSS_COEFF = 0.7
ACCELERATION = -0.5  # negative is downwards
R = 10
MARGIN = 50
SLEEP_MS = 20

done = False
right_wall = WIDTH / 2 - R
bottom_wall = -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Jumping ball")

turtle.listen()
turtle.onkeypress(set_done, "space")

m = turtle.Turtle()
m.shape("circle")
m.penup()
m.goto(WIDTH / 2, -HEIGHT / 2)
m.pendown()
m.setx(-WIDTH / 2)

vx = V
vy = 0
m.sety(HEIGHT / 3)


def tick():
    if not done:
        global vx, vy

        m.goto(m.xcor() + vx, m.ycor() + vy)

        # stop if the ball is about to leave the screen
        if m.xcor() > right_wall:
            set_done()

        if m.ycor() < bottom_wall:
            m.goto(m.xcor(), bottom_wall)
            vy *= -LOSS_COEFF

        vy += ACCELERATION

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
