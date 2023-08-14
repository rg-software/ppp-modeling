import turtle

WIDTH = 600
HEIGHT = 400

YEARS = 40
P = 1000
r = 0.2
K = 3000
HARVEST = 140


def setup_screen(title):
    turtle.setup(WIDTH, HEIGHT)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, YEARS, K)


setup_screen("The tragedy of the commons")

drawer = turtle.Turtle()
drawer.hideturtle()

for year in range(0, YEARS):
    drawer.goto(year, P)
    P += r * P * (1 - P / K)
    P = max(0, P - HARVEST)

turtle.update()
turtle.done()
