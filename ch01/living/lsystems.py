import turtle
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400

# Prusinkiewicz & Lindenmayer, Fig. 1.24-f
AXIOM = "X"
RULES = {"X": "g-[[X]+X]+g[+gX]-X", "g": "gg"}
ANGLE = 22.5
DISTANCE = 5
STEPS = 5

# Prusinkiewicz & Lindenmayer, Fig. 1.24-d
# AXIOM = "X"
# RULES = {"X": "g[+X]g[-X]+X", "g": "gg"}
# ANGLE = 20
# DISTANCE = 2
# STEPS = 7

# Prusinkiewicz & Lindenmayer, Fig. 1.24-c
# AXIOM = "g"
# RULES = {"g": "gg-[-g+g+g]+[+g-g-g]"}
# ANGLE = 22.5
# DISTANCE = 5
# STEPS = 4

# Prusinkiewicz & Lindenmayer, Fig. 1.24-e
# AXIOM = "X"
# RULES = {"X": "g[+X][-X]gX", "g": "gg"}
# ANGLE = 25.7
# DISTANCE = 2
# STEPS = 7

# Prusinkiewicz & Lindenmayer, Fig. 1.10 (Dragon curve)
# AXIOM = "f"
# RULES = {"f": "f+g", "g": "f-g"}
# ANGLE = 90
# DISTANCE = 10
# STEPS = 7

# Prusinkiewicz & Lindenmayer, Fig. 1.6 (Koch island)
# AXIOM = "g-g-g-g"
# RULES = {"g": "g-g+g+gg-g-g+g"}
# DISTANCE = 4
# ANGLE = 90
# STEPS = 3

# a simple plant
# AXIOM = "g"
# RULES = {"g": "g[+g][-g]"}
# ANGLE = 20
# DISTANCE = 25
# STEPS = 6

# a simple plant with a bud
# AXIOM = "A"
# RULES = {"A": "g[+A][-A]"}
# ANGLE = 20
# DISTANCE = 25
# STEPS = 6

# the LRI plant with a bud
# AXIOM = "A"
# RULES = {"A": "ALRI", "I": "g", "L": "[+g]", "R": "[-g]"}
# ANGLE = 30
# DISTANCE = 20
# STEPS = 4

# another example plant
# AXIOM = "X"  # "g"
# RULES = {"X": "g[+X]g[-X]+X", "g": "gg"}
# ANGLE = 40
# DISTANCE = 3
# STEPS = 6


def setup_screen(title):
    turtle.setup(WIDTH, HEIGHT)
    turtle.tracer(0, 0)
    turtle.title(title)


@dataclass
class LSystem:
    script: str

    @classmethod
    def create(cls):
        r = cls(AXIOM)
        for _ in range(STEPS):
            r.transform()
        return r

    def apply_rule(self, c):
        return c if c not in RULES else RULES[c]

    def transform(self):
        self.script = "".join([self.apply_rule(c) for c in self.script])

    def draw(self, pos, angle):
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.penup()
        # print(pos)
        drawer.goto(pos)
        drawer.pendown()
        drawer.setheading(angle)

        while self.script:
            c = self.script[0]
            self.script = self.script[1:]

            if c.islower():
                drawer.forward(DISTANCE)
                turtle.update()
            if c == "+":
                drawer.left(ANGLE)
            if c == "-":
                drawer.right(ANGLE)
            if c == "[":
                self.draw(drawer.pos(), drawer.heading())
            if c == "]":
                return


setup_screen("L-systems")
s = LSystem.create()
s.draw((0, -HEIGHT / 2), 90)
turtle.done()
