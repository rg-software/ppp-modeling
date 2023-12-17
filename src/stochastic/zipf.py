import math
import turtle
from collections import defaultdict
from pydoc_data.topics import topics

WIDTH = 600
HEIGHT = 400


def setup_screen(title, width, height):
    turtle.setup(WIDTH, HEIGHT)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, math.ceil(width), math.ceil(height))


input_text = " ".join(topics.values())
words = input_text.split()
freq = defaultdict(int)

for word in [w.lower() for w in words if w.isalnum()]:
    freq[word] += 1

values = sorted(freq.values(), reverse=True)

setup_screen("Zipf's law", math.log(len(values)), math.log(values[0]))
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()

for x, y in enumerate(values):
    drawer.goto(math.log(x + 1), math.log(y))
    drawer.pendown()

turtle.update()
turtle.done()
