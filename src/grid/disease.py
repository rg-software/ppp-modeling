import turtle
from enum import Enum
from random import randint, uniform
from dataclasses import dataclass

H = 41
W = 41
SLEEP_MS = 20
CELLSIZE = 10  # pixels
SHAPE_SIZE = CELLSIZE / 20  # turtle size

IMMUNE_DURATION = 14
INFECTED_DURATION = 7
PINHABIT = 0.3  # probability for a cell to be inhabited
PINFECT = 0.5  # probability for a cell to be infected by a neighbor


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

    def x(self):
        return int(self.shape.xcor())

    def y(self):
        return int(self.shape.ycor())

    @classmethod
    def populate(cls, x, y):
        if uniform(0, 1) > PINHABIT and not (x == W // 2 and y == H // 2):
            return None
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.color("green")
        return cls(p, Status.HEALTHY, 0)

    def update_status(self, status, count):
        self.status = status
        self.count = count

        colors = {
            Status.HEALTHY: "green",
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
                self.update_status(Status.IMMUNE, IMMUNE_DURATION)

    def moved_to(self, x, y):
        self.shape.goto(x, y)
        return self


@dataclass
class WorldState:
    cells: list

    def spread_from(self, x, y):
        r = []
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                cell = self.cells[xn % W][yn % H]
                is_healthy = cell and cell.status == Status.HEALTHY
                if is_healthy and uniform(0, 1) <= PINFECT:
                    r.append(cell)

        return r

    def move(self, p):
        newx = randint(p.x() - 1, p.x() + 1) % W
        newy = randint(p.y() - 1, p.y() + 1) % H

        if not self.cells[newx][newy]:
            self.cells[p.x()][p.y()] = None
            self.cells[newx][newy] = p.moved_to(newx, newy)

    def print_stats(self, people):
        healthy = len([p for p in people if p.status == Status.HEALTHY])
        infected = len([p for p in people if p.status == Status.INFECTED])
        immune = len([p for p in people if p.status == Status.IMMUNE])
        print(f"{healthy}\t{infected}\t{immune}")

    def update(self):
        to_infect = []
        people = sum(([v for v in self.cells[x] if v] for x in range(W)), [])
        self.print_stats(people)

        for p in people:
            p.update()
            self.move(p)

            if p.status == Status.INFECTED:
                to_infect += self.spread_from(p.x(), p.y())

        for c in to_infect:
            c.update_status(Status.INFECTED, INFECTED_DURATION)

    @classmethod
    def setup(cls):
        cells = [[Cell.populate(x, y) for y in range(H)] for x in range(W)]
        cells[W // 2][H // 2].update_status(Status.INFECTED, INFECTED_DURATION)
        return cls(cells)


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Spread of disease")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
