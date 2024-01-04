import turtle
import math
from enum import Enum
from random import uniform
from dataclasses import dataclass

H = 41
W = 41
SLEEP_MS = 20
CELLSIZE = 10  # pixels
SHAPE_SIZE = CELLSIZE / 20  # turtle size
WIND_DIRECTION = math.pi / 4
WIND_STRENGTH = 0.5
P = 0.6
PTREE = 0.6


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
    TREE = 1
    FIRE = 2
    EMPTY = 3


@dataclass
class Land:
    shape: turtle.Turtle
    status: Status = Status.EMPTY

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        status = Status.TREE if uniform(0, 1) <= PTREE else Status.EMPTY
        return cls(p).update_status(status)

    def update_status(self, status):
        self.status = status
        colors = {Status.TREE: "green", Status.FIRE: "red", Status.EMPTY: "white"}
        self.shape.color(colors[status])
        return self


@dataclass
class WorldState:
    cells: list

    def spread_from(self, x, y):
        r = []
        for xn in range(max(0, x - 1), min(x + 2, W)):
            for yn in range(max(0, y - 1), min(y + 2, H)):
                a = math.atan2(yn - y, xn - x) - WIND_DIRECTION
                p = P + P * WIND_STRENGTH * math.cos(a)
                neighbor = self.cells[xn][yn]
                if neighbor.status == Status.TREE and uniform(0, 1) <= p:
                    r.append(neighbor)

        return r

    def update(self):
        to_burn = []
        for x in range(W):
            for y in range(H):
                if self.cells[x][y].status == Status.FIRE:
                    to_burn += self.spread_from(x, y)
                    self.cells[x][y].update_status(Status.EMPTY)

        for c in to_burn:
            c.update_status(Status.FIRE)

    @classmethod
    def setup(cls):
        cells = [[Land.create(x, y) for y in range(H)] for x in range(W)]
        cells[W // 2][H // 2].update_status(Status.FIRE)
        return cls(cells)


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Forest fire")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
