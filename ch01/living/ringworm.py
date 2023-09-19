import turtle
from enum import Enum
from random import randint
from dataclasses import dataclass

H = 41
W = 41
SLEEP_MS = 20
CELLSIZE = 10  # pixels
SHAPE_SIZE = CELLSIZE / 20  # turtle size


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


class Status(Enum):
    HEALTHY = 1
    INFECTED = 2
    IMMUNE = 3


@dataclass
class Cell:
    shape: turtle.Turtle
    status: Status
    count: int

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.color("white")
        return cls(p, Status.HEALTHY, 0)

    def update_status(self, status, count):
        self.status = status
        self.count = count

        colors = {
            Status.HEALTHY: "white",
            Status.INFECTED: "red",
            Status.IMMUNE: "blue",
        }
        self.shape.color(colors[status])

    def update(self):
        self.count = max(0, self.count - 1)
        if self.count == 0:
            if self.status == Status.IMMUNE:
                self.update_status(Status.HEALTHY, 0)
            elif self.status == Status.INFECTED:
                self.update_status(Status.IMMUNE, 4)


@dataclass
class WorldState:
    cells: list

    def spread_from(self, x, y):
        r = []
        for xn in range(max(0, x - 1), min(x + 2, W)):
            for yn in range(max(0, y - 1), min(y + 2, H)):
                if self.cells[xn][yn].status == Status.HEALTHY and randint(0, 1) == 0:
                    r.append(self.cells[xn][yn])

        return r

    def update(self):
        for x in range(W):
            for y in range(H):
                self.cells[x][y].update()

        to_infect = []
        for x in range(W):
            for y in range(H):
                if self.cells[x][y].status == Status.INFECTED:
                    to_infect += self.spread_from(x, y)

        for c in to_infect:
            c.update_status(Status.INFECTED, 6)

    @classmethod
    def setup(cls):
        cells = [[Cell.create(x, y) for y in range(H)] for x in range(W)]
        cells[W // 2][H // 2].update_status(Status.INFECTED, 6)
        return cls(cells)


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Ringworm infection")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
