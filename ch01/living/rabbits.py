import turtle
from random import uniform, randint
from dataclasses import dataclass

H = 20
W = 30
SLEEP_MS = 20

GRASS_GROWTH_SPEED = 0.02
RABBITS = 40
WOLVES = 10

MIN_DELIVERY_FAT = 0.7
NEWBORN_FAT = 0.5


@dataclass
class RabbitCfg:
    eat_speed: float = 0.25
    max_age: int = 15
    delivery_age: int = 3
    delivery_p = 0.7
    fat_factor = 1
    shape: str = "turtle"
    color: str = "rosy brown"


@dataclass
class WolfConfig:
    eat_speed: float = 0.01
    max_age: int = 30
    delivery_age: int = 5
    delivery_p = 0.5
    fat_factor = 0.25
    shape: str = "triangle"
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
    m: turtle.Turtle

    def update(self, fat, is_alive):
        if not is_alive:
            self.m.hideturtle()
        else:
            self.m.shapesize(fat)

    def move(self, coords):
        self.m.goto(coords[1], coords[0])

    @classmethod
    def create(cls, shape, color, size, coords):
        m = turtle.Turtle()
        m.shape(shape)
        m.color(color)
        m.penup()
        m.shapesize(size)
        m.goto(coords[1], coords[0])
        return cls(m)


@dataclass
class Grass:
    shape: Shape
    fat: float

    def grow(self):
        self.fat = min(self.fat + GRASS_GROWTH_SPEED, 1)
        self.shape.update(self.fat, True)

    def try_eat(self, to_eat):
        r = min(to_eat, self.fat)
        self.fat -= r
        return r

    @classmethod
    def create(cls, coords):
        fat = uniform(0, 1)
        return cls(Shape.create("circle", "lawn green", fat, coords), fat)


@dataclass
class Critter:
    shape: Shape
    fat: float
    age: int
    cfg: object

    def grow(self, food):
        self.fat = max(0, self.fat - self.cfg.eat_speed)
        self.age += 1

        if self.is_alive() and food:
            food_needed = (1.0 - self.fat) / self.cfg.fat_factor
            if (r := food.try_eat(food_needed)) > 0:
                self.fat += r * self.cfg.fat_factor
        self.shape.update(self.fat, self.is_alive())

    def move(self, coords):
        self.shape.move(coords)

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
        return None if fail else Critter.create_full(self.cfg, 0, NEWBORN_FAT, coords)

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

    def things(self, plane):
        return list((key, value) for key, value in plane.items() if value)

    def keep_alive(self, plane):
        plane.update({k: None for k, v in self.things(plane) if not v.is_alive()})

    def move_and_deliver(self, plane):
        for coords, v in self.things(plane):
            r, c = coords
            newcoords = randint(r - 1, r + 1) % H, randint(c - 1, c + 1) % W
            if not plane[newcoords]:
                plane[coords] = v.deliver_at(coords)
                plane[newcoords] = v
                v.move(newcoords)

    def update(self):
        self.cycle += 1
        things_r = self.things(self.rabbits)
        things_w = self.things(self.wolves)
        print(f"{self.cycle}\t{len(things_r)}\t{len(things_w)}")

        for coords, v in self.things(self.grass):
            v.grow()

        for coords, v in things_r:
            v.grow(self.grass[coords])

        for coords, v in things_w:
            v.grow(self.rabbits[coords])

        self.keep_alive(self.rabbits)
        self.keep_alive(self.wolves)

        self.move_and_deliver(self.rabbits)
        self.move_and_deliver(self.wolves)

    @classmethod
    def coords(cls, count):
        r = set()
        while len(r) < count:
            r.add((randint(0, H - 1), randint(0, W - 1)))
        return r

    @classmethod
    def setup(cls):
        coords = [(r, c) for c in range(W) for r in range(H)]

        grass = {c: Grass.create(c) for c in coords}
        rabbits = {c: None for c in coords}
        wolves = {c: None for c in coords}

        rabbits.update({c: Critter.create(RabbitCfg(), c) for c in cls.coords(RABBITS)})
        wolves.update({c: Critter.create(WolfConfig(), c) for c in cls.coords(WOLVES)})

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
