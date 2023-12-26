import math
import turtle
from random import randint
from dataclasses import dataclass

H = 25
W = 25
SLEEP_MS = 50
CELLSIZE = 20  # pixels

SHAPE_SIZE_FACTOR = 0.01
SHAPE_SIZE = SHAPE_SIZE_FACTOR * CELLSIZE / 20  # turtle size
POPULATION = 25000
DAC = 0.00005


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
            self.shape.shapesize(SHAPE_SIZE * math.sqrt(self.population))

    def score(self):
        return self.population - DAC * self.population**2

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.goto(x, y)
        return cls(p)


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
    prev_ranks: list = None

    @classmethod
    def setup(cls):
        cells = [[City.create(x, y) for y in range(H)] for x in range(W)]
        population = [Person.create(cells) for _ in range(POPULATION)]
        return cls(cells, population)

    def better_neighbor(self, city, dist):
        best_city = city
        xc, yc = int(city.shape.xcor()), int(city.shape.ycor())
        for x in range(max(0, xc - dist), min(W - 1, xc + dist) + 1):
            for y in range(max(0, yc - dist), min(H - 1, yc + dist) + 1):
                dst = self.cities[x][y]
                if dst.score() > best_city.score():
                    best_city = dst
        return best_city

    def rankings(self):
        scores = [self.cities[x][y].population for x in range(W) for y in range(H)]
        return sorted([v for v in scores if v > 0], reverse=True)

    def update(self):
        for p in self.population:
            dest = self.better_neighbor(p.city, p.max_distance)
            p.move_to(dest)

        if self.rankings() == self.prev_ranks:
            print(f"The cities ({len(self.prev_ranks)}) have stabilized")
        self.prev_ranks = self.rankings()


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


def draw_chart(rankings):
    # TODO(mm): get rid of clearscreen()?
    turtle.clearscreen()
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.penup()

    width = math.log(len(rankings))
    height = math.log(rankings[0])
    turtle.setworldcoordinates(0, 0, math.ceil(width), math.ceil(height))

    print(rankings)
    for x, y in enumerate(rankings):
        drawer.goto(math.log(x + 1), math.log(y))
        drawer.pendown()


setup_screen("The rise of cities")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)
    else:
        draw_chart(world_state.rankings())


tick()
turtle.done()
