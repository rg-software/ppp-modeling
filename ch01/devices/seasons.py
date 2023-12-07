import turtle
from random import choices

CELLSIZE = 20
SHAPE_SIZE = CELLSIZE / 20
DAYS_IN_SEASON = 20
DAYS = 4 * DAYS_IN_SEASON

state = "sunny"
seasons = ("sunny", "rainy", "cloudy", "snowy")
colors = {"sunny": "yellow", "cloudy": "gray", "rainy": "black", "snowy": "white"}
winter = {"sunny": 0.25, "cloudy": 0.05, "rainy": 0.05, "snowy": 0.65}
spring = {"sunny": 0.4, "cloudy": 0.28, "rainy": 0.3, "snowy": 0.02}
summer = {"sunny": 0.6, "cloudy": 0.2, "rainy": 0.2, "snowy": 0}
autumn = {"sunny": 0.3, "cloudy": 0.28, "rainy": 0.4, "snowy": 0.02}


def setup_screen(title):
    turtle.setup(800, 600)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(-1, -12, DAYS_IN_SEASON, 8)


def weight_to(pweights, src, dest):
    if dest == src:
        return pweights[src]
    r = 1.0 - pweights[src]
    wsum = sum(pweights[k] for k in pweights if k != src)
    return r * pweights[dest] / wsum


def next_day(src, pweights):
    wlist = [weight_to(pweights, src, dest) for dest in seasons]
    return choices(seasons, tuple(wlist))[0]


def lerp(beg, end, day):
    return beg + (day / (DAYS_IN_SEASON - 1)) * (end - beg)


def pweights_for(day):
    year = [winter, spring, summer, autumn, winter]
    cur_season = day // DAYS_IN_SEASON
    season_day = day % DAYS_IN_SEASON

    cur_pweights = year[cur_season]
    next_pweights = year[cur_season + 1]

    return {k: lerp(cur_pweights[k], next_pweights[k], season_day) for k in seasons}


setup_screen("The Four Seasons")

for day in range(DAYS):
    drawer = turtle.Turtle()
    drawer.penup()
    drawer.shapesize(SHAPE_SIZE)
    drawer.shape("circle")
    drawer.forward(day % DAYS_IN_SEASON)
    drawer.right(90)
    drawer.forward(day // DAYS_IN_SEASON)
    drawer.color("black", colors[state])
    state = next_day(state, pweights_for(day))

# s = winter
# print([weight_to(s, "sunny", dest) for dest in seasons])
# print([weight_to(s, "rainy", dest) for dest in seasons])
# print([weight_to(s, "cloudy", dest) for dest in seasons])
# print([weight_to(s, "snowy", dest) for dest in seasons])

turtle.update()
turtle.done()
