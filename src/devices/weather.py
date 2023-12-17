import turtle
from random import choices

CELLSIZE = 20
SHAPE_SIZE = CELLSIZE / 20
DAYS = 20


def setup_screen(title):
    turtle.setup(800, 600)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(-1, -10, DAYS, 10)


setup_screen("Markovian weather")


def next_day(state):
    rules = {
        "sunny": (("sunny", "rainy", "cloudy"), (0.6, 0.1, 0.3)),
        "cloudy": (("cloudy", "sunny", "rainy"), (0.5, 0.3, 0.2)),
        "rainy": (("rainy", "sunny", "cloudy"), (0.4, 0.3, 0.3)),
    }
    states, weights = rules[state]
    return choices(states, weights)[0]


state = "sunny"
colors = {"sunny": "yellow", "cloudy": "gray", "rainy": "black"}

for day in range(DAYS):
    drawer = turtle.Turtle()
    drawer.penup()
    drawer.shapesize(SHAPE_SIZE)
    drawer.shape("circle")
    drawer.forward(day)
    drawer.color("black", colors[state])
    state = next_day(state)

turtle.update()
turtle.done()
