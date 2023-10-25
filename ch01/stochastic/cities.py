import math
import turtle
from random import randint
from dataclasses import dataclass


H = 15
W = 15
SLEEP_MS = 50
CELLSIZE = 30  # pixels
SHAPE_SIZE = CELLSIZE / 20  # turtle size
POPULATION = 15000
SHAPE_SIZE_FACTOR = 5000
DA_FORCE_COEFF = 0.00001


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
class City:
    shape: turtle.Turtle
    population: int = 0

    def increase(self):
        self.update(self.population + 1)

    def decrease(self):
        self.update(self.population - 1)

    def update(self, p):
        self.population = p

        if self.population == 0:
            self.shape.hideturtle()
        else:
            self.shape.shapesize(SHAPE_SIZE * self.population / SHAPE_SIZE_FACTOR)

    def value(self):
        return self.population - DA_FORCE_COEFF * self.population**2

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.goto(x, y)
        return cls(p)


# agents gravitate
# towards high-density locations because such locations generate positive externalities,
# which have been shown empirically to be the driving force behind the formation of
# agglomeration economies in the US
# S (see, e.g., Rosenthal & Strange, 2001).

# s bounded rationality in the form of limited spatial reach

# state of location updated on the basis of neighbors at most D away
# each agent has capability to migrate within a threshold r
# then the decision depends on its reach and state of neighbors

# start with cities in a grid, agents are randomly distributed
# also each agent has builtin visibility reach (up to half size)

# attractiveness is population - c*population^2 (negative effect is there too)
# (and negatives must outweight at some point)
# on each turn agents migrate

# 12000 agents; the least mobile travel 1 unit dist; most mobile travel everywhere


@dataclass
class Person:
    city: object
    max_distance: int

    def move_to(self, new_city):
        self.city.decrease()
        self.city = new_city
        new_city.increase()

    @classmethod
    def create(cls, cities):
        c = cities[randint(0, W - 1)][randint(0, H - 1)]
        c.increase()
        return cls(c, randint(1, max(H, W) // 2))


@dataclass
class WorldState:
    cities: list
    population: list

    @classmethod
    def setup(cls):
        cells = [[City.create(x, y) for y in range(H)] for x in range(W)]
        population = [Person.create(cells) for _ in range(POPULATION)]
        return cls(cells, population)

    def better_neighbor(self, city, dist):
        bestcity = city
        xc, yc = int(city.shape.xcor()), int(city.shape.ycor())
        for x in range(max(0, xc - dist), min(W - 1, xc + dist)):
            for y in range(max(0, yc - dist), min(H - 1, yc + dist)):
                dst = self.cities[x][y]
                if dst.value() > bestcity.value():
                    bestcity = dst
        return bestcity

    def rankings(self):
        values = [self.cities[x][y].population for x in range(W) for y in range(H)]
        return sorted([v for v in values if v > 0], reverse=True)

    def update(self):
        for p in self.population:
            dest = self.better_neighbor(p.city, p.max_distance)
            p.move_to(dest)

        print(self.rankings())


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Cities")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)
    else:
        turtle.clearscreen()
        drawer = turtle.Turtle()
        drawer.hideturtle()

        values = world_state.rankings()
        width = math.log(len(values))
        height = math.log(values[0])
        turtle.setworldcoordinates(0, 0, math.ceil(width), math.ceil(height))

        for x, y in enumerate(values):
            drawer.goto(math.log(x + 1), math.log(y))


tick()
turtle.done()
