import turtle
from random import uniform, randint
from dataclasses import dataclass

H = 20  # grass patch size
W = 30
SLEEP_MS = 20

GRASS_GROWTH = 0.02  # units per step
RABBITS = 40
WOLVES = 10

MIN_DELIVERY_FAT = 0.7  # needed to deliver an offspring
NEWBORN_FAT = 0.5


# fine-tunable parameters of rabbits and wolves
@dataclass
class RabbitCfg:
    fat_use: float = 0.25
    max_age: int = 15
    delivery_age: int = 3
    delivery_p = 0.7
    fat_factor = 1
    shape: str = "turtle"
    color: str = "rosy brown"


@dataclass
class WolfConfig:
    fat_use: float = 0.01
    max_age: int = 30
    delivery_age: int = 5
    delivery_p = 0.5
    fat_factor = 0.25
    shape: str = "classic"
    color: str = "black"


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
class Shape:
    drawer: turtle.Turtle

    def update(self, fat, is_alive):
        if not is_alive:
            self.drawer.hideturtle()
        else:
            self.drawer.shapesize(fat)

    def move(self, coords):
        self.drawer.goto(coords[0], coords[1])

    @classmethod
    def create(cls, shape, color, size, coords):
        r = turtle.Turtle()
        r.shape(shape)
        r.color(color)
        r.penup()
        r.shapesize(size)
        r.goto(coords[0], coords[1])
        r.right(90)
        return cls(r)


@dataclass
class Grass:
    shape: Shape
    amount: float

    def grow(self):
        self.amount = min(self.amount + GRASS_GROWTH, 1)
        self.shape.update(self.amount, True)

    def try_eat(self, to_eat):
        r = min(to_eat, self.amount)
        self.amount -= r
        return r

    @classmethod
    def create(cls, coords):
        amount = uniform(0, 1)
        return cls(Shape.create("circle", "lawn green", amount, coords), amount)


@dataclass
class Animal:
    shape: Shape
    fat: float
    age: int
    cfg: object

    def update_fat(self, food):
        self.fat = max(0, self.fat - self.cfg.fat_use)
        self.age += 1

        if self.is_alive() and food:
            food_needed = (1.0 - self.fat) / self.cfg.fat_factor
            if (r := food.try_eat(food_needed)) > 0:
                self.fat += r * self.cfg.fat_factor
        self.shape.update(self.fat, self.is_alive())

    def moved_to(self, coords):
        self.shape.move(coords)
        return self

    def try_eat(self, to_eat):
        r = 0 if to_eat < self.fat else self.fat
        self.fat -= r
        self.shape.update(self.fat, self.is_alive())
        return r

    def is_alive(self):
        return self.fat > 0 and self.age <= self.cfg.max_age

    def deliver_at(self, coords):
        fat_age_fail = self.fat < MIN_DELIVERY_FAT or self.age < self.cfg.delivery_age
        fail = fat_age_fail or uniform(0, 1) > self.cfg.delivery_p
        return None if fail else Animal.create_full(self.cfg, 0, NEWBORN_FAT, coords)

    @classmethod
    def create_full(cls, cfg, age, fat, coords):
        shape = Shape.create(cfg.shape, cfg.color, fat, coords)
        return cls(shape, fat, age, cfg)

    @classmethod
    def create(cls, cfg, coords):
        return cls.create_full(cfg, randint(0, cfg.max_age), uniform(0, 1), coords)


@dataclass
class WorldState:
    grass: dict
    rabbits: dict
    wolves: dict
    cycle: int

    # get all non-None objects
    def animals(self, plane):
        return list((key, value) for key, value in plane.items() if value)

    def keep_alive(self, plane):
        plane.update({k: None for k, v in self.animals(plane) if not v.is_alive()})

    def move_and_deliver(self, plane):
        for coords, v in self.animals(plane):
            x, y = coords
            newcoords = randint(x - 1, x + 1) % W, randint(y - 1, y + 1) % H
            if not plane[newcoords]:
                plane[newcoords] = v.moved_to(newcoords)
                plane[coords] = v.deliver_at(coords)

    def update(self):
        self.cycle += 1
        rabbits = self.animals(self.rabbits)
        wolves = self.animals(self.wolves)
        print(f"{self.cycle}\t{len(rabbits)}\t{len(wolves)}")

        for v in self.grass.values():
            v.grow()

        for coords, v in rabbits:
            v.update_fat(self.grass[coords])

        for coords, v in wolves:
            v.update_fat(self.rabbits[coords])

        self.keep_alive(self.rabbits)
        self.keep_alive(self.wolves)

        self.move_and_deliver(self.rabbits)
        self.move_and_deliver(self.wolves)

    @classmethod
    def coords(cls, count):
        r = set()
        while len(r) < count:
            r.add((randint(0, W - 1), randint(0, H - 1)))
        return r

    @classmethod
    def setup(cls):
        coords = [(x, y) for x in range(W) for y in range(H)]

        grass = {c: Grass.create(c) for c in coords}
        rabbits = {c: None for c in coords}
        wolves = {c: None for c in coords}

        rabbits.update({c: Animal.create(RabbitCfg(), c) for c in cls.coords(RABBITS)})
        wolves.update({c: Animal.create(WolfConfig(), c) for c in cls.coords(WOLVES)})

        return cls(grass, rabbits, wolves, 0)


def setup_screen(title):
    turtle.setup(W * 20, H * 20)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Rabbits and wolves")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
