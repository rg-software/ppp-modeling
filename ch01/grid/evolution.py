import turtle
from random import randint, choices
from dataclasses import dataclass

H = 40  # grass patch size
W = 70
SLEEP_MS = 20
CELLSIZE = 10  # pixels
SHAPE_SIZE = CELLSIZE / 20  # turtle size

INITIAL_ENERGY = 120
MAX_ENERGY = 400
FISSION_ENERGY = 250
MATURITY_AGE = 200
FOOD_ENERGY = 20
MAX_WEIGHT = 32
EDEN_WIDTH = 20
EDEN_MARGIN = 10
PLANKTON_PERIOD = 2
PLANKTON_COUNT = 100
BUGS_COUNT = 10


gen_count = []  # bugs in the given generation
gen_visited = []  # unique cells visited by bugs of a generation


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


def clamp(v, min_v, max_v):
    return min(max_v, max(min_v, v))


@dataclass
class Plankton:
    shape: turtle.Turtle

    def energy(self):
        return FOOD_ENERGY if self.shape.isvisible() else 0

    def show(self, s):
        if s:
            self.shape.showturtle()
        else:
            self.shape.hideturtle()

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.color("lawn green")
        p.shape("triangle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.hideturtle()
        return cls(p)


@dataclass
class Bug:
    shape: turtle.Turtle
    dirweights: list
    energy: int
    generation: int
    visited: set
    age: int = 0

    def x(self):
        return round(self.shape.xcor())

    def y(self):
        return round(self.shape.ycor())

    def remove(self):
        gen_visited[self.generation] += len(self.visited)
        self.shape.hideturtle()
        visits = [f"{gen_visited[i]/gen_count[i]:.2f}" for i in range(len(gen_count))]

        print("Visits: " + " ".join(visits))
        print(f"Profile: {self.dirweights}\n")

    def eat_and_move(self, food):
        self.visited.add((self.x(), self.y()))
        self.age += 1
        self.energy -= 1
        if self.energy == 0:
            self.remove()
        else:
            self.energy = min(MAX_ENERGY, self.energy + food)
            r = choices(list(range(8)), self.dirweights)[0]
            self.shape.left(45 * r)
            self.shape.forward(1)
            self.shape.setx(clamp(self.shape.xcor(), 0, W - 1))
            self.shape.sety(clamp(self.shape.ycor(), 0, H - 1))

    def new_dirweights(self, dirs, d):
        idx = randint(0, 7)
        newdirs = list(dirs)
        newdirs[idx] = clamp(int(dirs[idx] * d), 1, MAX_WEIGHT)
        return newdirs

    def fission(self):
        if self.age > MATURITY_AGE and self.energy > FISSION_ENERGY:
            self.remove()
            e = int(self.energy / 2)
            dirs1 = self.new_dirweights(self.dirweights, 2)
            dirs2 = self.new_dirweights(self.dirweights, 0.5)

            return [
                Bug.create(self.x(), self.y(), dirs1, e, self.generation + 1),
                Bug.create(self.x(), self.y(), dirs2, e, self.generation + 1),
            ]
        return [self]

    @classmethod
    def create(cls, x, y, weights, energy, gen):
        if gen == len(gen_count):
            print(f"Generation: {gen}")
            gen_count.append(0)
            gen_visited.append(0)
        gen_count[gen] += 1

        p = turtle.Turtle()
        p.penup()
        p.shape("turtle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        return cls(p, weights, energy, gen, set())

    @classmethod
    def create_random(cls):
        x = randint(0, W - 1)
        y = randint(0, H - 1)
        weights = [randint(1, MAX_WEIGHT) for _ in range(8)]
        return cls.create(x, y, weights, INITIAL_ENERGY, 0)


@dataclass
class WorldState:
    plankton: list
    bugs: list
    cycle: int

    def add_plankton(self, count=1):
        for _ in range(count):
            x, y = randint(0, W - 1), randint(0, H - 1)
            ex, ey = randint(EDEN_MARGIN, EDEN_WIDTH), randint(EDEN_MARGIN, EDEN_WIDTH)

            self.plankton[x][y].show(True)  # add to the bowl
            self.plankton[ex][ey].show(True)  # add to the garden
        return self

    def update(self):
        self.cycle += 1

        if self.cycle % PLANKTON_PERIOD == 0:
            self.add_plankton()

        for b in self.bugs:
            food = self.plankton[b.x()][b.y()]
            b.eat_and_move(food.energy())
            food.show(False)

        self.bugs = [b for b in self.bugs if b.energy > 0]
        self.bugs = sum((b.fission() for b in self.bugs), [])

    @classmethod
    def setup(cls):
        bugs = [Bug.create_random() for _ in range(BUGS_COUNT)]
        plankton = [[Plankton.create(x, y) for y in range(H)] for x in range(W)]

        return cls(plankton, bugs, 0).add_plankton(PLANKTON_COUNT)


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Evolution")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
