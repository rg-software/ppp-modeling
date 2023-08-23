# chk % of fissions by generation

import turtle
from random import randint
from dataclasses import dataclass, field

H = 40  # grass patch size
W = 70
SLEEP_MS = 20
CELLSIZE = 10
SHAPE_SIZE = CELLSIZE / 20

INITIAL_ENERGY = 250 / 2  # 30
MAX_ENERGY = 370
FISSION_ENERGY = 250
MATURITY_AGE = 200
FOOD_ENERGY = 20
MAX_WEIGHT = 16 * 2
GARDEN_WIDTH = 15
PERIOD = 3
PLANKTON_COUNT = 200

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.goto(0, 0)

from collections import defaultdict

bugs_count = defaultdict(int)  # by gen
fis_count = defaultdict(int)  # by gen
starved_count = defaultdict(int)
starved_age = defaultdict(int)
dist = defaultdict(int)


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
        # p.setundobuffer(None)
        # self.plankton[(x, y)] = p


@dataclass
class Bug:
    shape: turtle.Turtle
    dirweights: list
    energy: int  # = INITIAL_ENERGY
    generation: int
    age: int = 0
    visited: set = field(default_factory=set)

    def coords(self):
        return (int(self.shape.xcor()), int(self.shape.ycor()))

    def weighted_random(self):  # pairs):
        cnt = 0
        total = sum(self.dirweights)
        r = randint(1, total)
        for weight in self.dirweights:
            r -= weight
            if r <= 0:
                return cnt
            cnt += 1
        raise RuntimeError("error")

    def eat_and_move(self, food):
        self.visited.add((int(self.shape.xcor()), int(self.shape.ycor())))
        self.age += 1
        self.energy -= 1
        if self.energy == 0:
            starved_count[self.generation] += 1
            starved_age[self.generation] += self.age
            dist[self.generation] += len(self.visited)
            self.shape.hideturtle()
        else:
            self.energy = min(MAX_ENERGY, self.energy + food)
            r = self.weighted_random()
            self.shape.left(45 * r)
            self.shape.forward(1.0)  # .5)
            self.shape.setx(clamp(self.shape.xcor(), 0, W - 1))
            self.shape.sety(clamp(self.shape.ycor(), 0, H - 1))

    def new_dirweights(self, dirs, d):
        idx = randint(0, 7)
        newdirs = list(dirs)
        newdirs[idx] = clamp(int(dirs[idx] * d), 1, MAX_WEIGHT)
        return newdirs

    def fission(self):
        if self.age > MATURITY_AGE and self.energy > FISSION_ENERGY:
            x = self.shape.xcor()
            y = self.shape.ycor()
            e = int(self.energy / 2)
            gen = self.generation + 1
            dirs1 = self.new_dirweights(self.dirweights, 2)
            dirs2 = self.new_dirweights(self.dirweights, 0.5)

            print(dirs1)
            print(dirs2)

            self.shape.hideturtle()

            dist[self.generation] += len(self.visited)
            fis_count[self.generation] += 1
            print("fission %")
            for g in bugs_count:
                print(f"{round(100*fis_count[g]/bugs_count[g],2)} ", end=" ")
            print("\nstarved age")
            for g in bugs_count:
                if starved_count[g] != 0:
                    print(f"{round(starved_age[g]/starved_count[g],2)} ", end=" ")
            print("\navg dist")
            for g in bugs_count:
                print(f"{round(dist[g]/bugs_count[g],2)} ", end=" ")
            print()

            return [Bug.create(x, y, dirs1, e, gen), Bug.create(x, y, dirs2, e, gen)]
        return [self]

    @classmethod
    def create(cls, x, y, lst, energy, gen):
        bugs_count[gen] += 1

        p = turtle.Turtle()
        p.penup()
        p.shape("turtle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        print(f"Created bug gen {gen}")
        return cls(p, lst, energy, gen)

    @classmethod
    def create_random(cls):
        x = randint(0, W - 1)
        y = randint(0, H - 1)
        weights = [randint(1, MAX_WEIGHT) for _ in range(8)]
        return cls.create(x, y, weights, INITIAL_ENERGY, 0)


@dataclass
class WorldState:
    plankton: dict
    bugs: list
    cycle: int

    def add_plankton(self):
        x, y = randint(0, W - 1), randint(0, H - 1)
        gx, gy = randint(0, GARDEN_WIDTH), randint(0, GARDEN_WIDTH)

        self.plankton[(x, y)].show(True)
        self.plankton[(gx, gy)].show(True)

    def update(self):
        writer.clear()
        writer.hideturtle()
        writer.write(f"{self.cycle} {len(turtle.turtles())}")

        self.cycle += 1

        if self.cycle % PERIOD == 0:
            self.add_plankton()

        for b in self.bugs:
            food = self.plankton[b.coords()]
            b.eat_and_move(food.energy())  # food.is_shown())
            food.show(False)

        self.bugs = [b for b in self.bugs if b.energy > 0]
        self.bugs = sum((b.fission() for b in self.bugs), [])

    @classmethod
    def setup(cls):
        coords = [(x, y) for x in range(W) for y in range(H)]

        bugs = [Bug.create_random() for _ in range(10)]  # bug count
        plankton = {c: Plankton.create(c[0], c[1]) for c in coords}

        r = cls(plankton, bugs, 0)
        for _ in range(PLANKTON_COUNT):
            r.add_plankton()

        return r


def setup_screen(title):
    turtle.setup(W * CELLSIZE, H * CELLSIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    # turtle.setundobuffer(None)
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
