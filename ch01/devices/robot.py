import turtle
from dataclasses import dataclass
from random import randint

WIDTH = 600
HEIGHT = 400
MARGIN = 50
SLEEP_MS = 1000


@dataclass
class SimState:
    done: bool = False

    def set_done(self):
        self.done = True

    @classmethod
    def setup(cls):
        r = cls()
        turtle.listen()
        turtle.onkeypress(r.set_done, "space")
        return r


@dataclass
class WorldState:
    input: str = ""
    state = "nuo"
    index: int = 0
    body = turtle.Turtle()
    arm = turtle.Turtle()
    box = turtle.Turtle()
    rules = {}

    def draw_state(self):
        self.arm.reset()
        self.arm.left({"l": 45, "r": -45, "n": 0}[self.state[0]])
        self.arm.color("red" if self.state[1] == "u" else "black")
        self.arm.shape("classic" if self.state[2] == "o" else "arrow")
        self.arm.forward(30)
        self.arm.left(180)

    def next(self):
        if r := self.index < len(self.input):
            print(f"Running {self.input[self.index]} in {self.state}")
            self.state = self.rules[(self.state, self.input[self.index])]
            self.index += 1
        return r

    def add_rules(self, src, dest, c1, c2):
        self.rules[(src, c1)] = dest
        self.rules[(dest, c2)] = src

    def add_all_rules(self, lst):
        for src, dest, c1, c2 in lst:
            self.add_rules(src, dest, c1, c2)

    def next_box(self):
        self.index = 0
        if randint(0, 1) == 0:  # small box
            self.box.shapesize(0.8)
            self.input = "DCURDOUL"
        else:
            self.box.shapesize(1.5)
            self.input = "DCULDOUR"

    @classmethod
    def setup(cls):
        r = cls()
        r.body.shape("circle")
        r.body.shapesize(2)
        r.arm.shapesize(3)
        r.box.penup()
        r.box.shape("square")
        r.box.forward(55)

        r.add_all_rules(
            [
                ("nuo", "ndo", "D", "U"),
                ("ndo", "ndc", "C", "O"),
                ("ndc", "nuc", "U", "D"),
                ("nuo", "nuc", "C", "O"),
                ("nuo", "ruo", "R", "L"),
                ("ruo", "rdo", "D", "U"),
                ("ruo", "ruc", "C", "O"),
                ("rdo", "rdc", "C", "O"),
                ("ruc", "rdc", "D", "U"),
                ("ruc", "nuc", "L", "R"),
                ("nuo", "luo", "L", "R"),
                ("luo", "ldo", "D", "U"),
                ("luo", "luc", "C", "O"),
                ("luc", "nuc", "R", "L"),
                ("luc", "ldc", "D", "U"),
                ("ldo", "ldc", "C", "O"),
            ]
        )

        return r


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


setup_screen("Robot control")
world_state = WorldState.setup()
sim_state = SimState.setup()


def tick():
    if not sim_state.done:
        try:
            if not world_state.next():
                world_state.next_box()

            world_state.draw_state()
            turtle.update()
            turtle.ontimer(tick, SLEEP_MS)
        except KeyError:
            print("Illegal command")


tick()
turtle.done()
