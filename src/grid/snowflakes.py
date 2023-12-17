import turtle
from dataclasses import dataclass

H = 201
W = 201
SLEEP_MS = 20
CELLSIZE = 4
SHAPE_SIZE = CELLSIZE / 20  # turtle size

ALPHA = 2.03
BETA = 0.4
GAMMA = 0.0001


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
class Drawer:
    shape: turtle.Turtle

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x + 0.5 * (y % 2), y)
        p.color("black")
        return cls(p)

    def update(self, v):
        self.shape.fillcolor(v, v, v)
        if SHAPE_SIZE * v == 0:
            self.shape.hideturtle()
        else:
            self.shape.showturtle()
            self.shape.shapesize(SHAPE_SIZE * v)


@dataclass
class WorldState:
    cells: list = None
    step: int = 0

    def make_cells(self, v):
        return [[v for _ in range(H)] for x in range(W)]

    def average(self, cells):
        avg = self.make_cells(0)

        for x in range(W):
            for y in range(H):
                e = cells[x][y]

                avg[x][y] += (1 - ALPHA * 0.5) * e
                for nx, ny in self.neighbors(x, y):
                    avg[nx][ny] += e * ALPHA / 12
        return avg

    def neighbors(self, x, y):
        even_neigh = [((x - 1) % W, (y - 1) % H), ((x - 1) % W, (y + 1) % H)]
        odd_neigh = [((x + 1) % W, (y - 1) % H), ((x + 1) % W, (y + 1) % H)]
        add_neighbors = even_neigh if y % 2 == 0 else odd_neigh

        return [
            (x, ((y + 1) % H)),
            (x, (y - 1) % H),
            ((x - 1) % W, y),
            ((x + 1) % W, y),
        ] + add_neighbors

    def receptive_cells_map(self):
        is_receptive = self.make_cells(False)

        for x in range(W):
            for y in range(H):
                if self.cells[x][y] >= 1:
                    for nx, ny in self.neighbors(x, y) + [(x, y)]:
                        is_receptive[nx][ny] = True

        return is_receptive

    def rec_nonrec_grids(self, is_receptive):
        receptive = self.make_cells(0)
        non_receptive = self.make_cells(0)

        for x in range(W):
            for y in range(H):
                e = self.cells[x][y]
                if is_receptive[x][y]:
                    receptive[x][y] = e + GAMMA
                else:
                    non_receptive[x][y] = e
        return receptive, non_receptive

    def update(self):
        self.step += 1

        is_receptive = self.receptive_cells_map()
        receptive, non_receptive = self.rec_nonrec_grids(is_receptive)
        non_receptive = self.average(non_receptive)

        for x in range(W):
            for y in range(H):
                self.cells[x][y] = receptive[x][y] + non_receptive[x][y]

    def fill_cells(self):
        self.cells = self.make_cells(BETA)
        self.cells[W // 2][H // 2] = 1.0
        return self

    @classmethod
    def setup(cls):
        return cls().fill_cells()


def setup_screen(title):
    turtle.colormode(1.0)
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


def update_shapes(shapes, cells):
    for x in range(W):
        for y in range(H):
            shapes[x][y].update(min(1, cells[x][y]))


setup_screen("Cellular snowflakes")
sim_state = SimState.setup()
world_state = WorldState.setup()
shapes = [[Drawer.create(x, y) for y in range(H)] for x in range(W)]


def tick():
    if not sim_state.done:
        world_state.update()
        if world_state.step % 50 == 0:
            print(f"step {world_state.step}")
            update_shapes(shapes, world_state.cells)
            turtle.update()

        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
