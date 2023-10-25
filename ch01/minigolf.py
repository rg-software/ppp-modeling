import turtle
import math
from random import uniform
from dataclasses import dataclass

WIDTH = 800
HEIGHT = 600
MIN_V = 5
MAX_V = 15
MIN_SIZE_FACTOR = 0.7
MAX_SIZE_FACTOR = 4
START_DISTANCE = 400
R = 10
MARGIN = 50
SLEEP_MS = 20


@dataclass
class SimState:
    done: bool

    def set_done(self):
        self.done = True

    @classmethod
    def setup(cls):
        r = cls(False)
        turtle.listen()
        turtle.onkey(r.set_done, "space")
        return r


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


# def draw_vessel():
#     m = turtle.Turtle()
#     m.hideturtle()
#     m.penup()
#     m.goto(-WIDTH / 2, -HEIGHT / 2)
#     m.pendown()
#     m.sety(HEIGHT / 2)
#     m.setx(WIDTH / 2)
#     m.sety(-HEIGHT / 2)
#     m.setx(-WIDTH / 2)


@dataclass
class Ball:
    m: turtle.Turtle
    # vx: float
    # vy: float
    #    r: float

    def move(self):
        # self.m.heading()
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if abs(self.m.xcor()) > WIDTH / 2 - self.r:
            self.vx *= -1

        if abs(self.m.ycor()) > HEIGHT / 2 - self.r:
            self.vy *= -1

    def mass(self):
        return math.pi * (self.r**2)

    @classmethod
    def create(cls):
        size = uniform(MIN_SIZE_FACTOR, MAX_SIZE_FACTOR)
        r = size * R
        x = uniform(-WIDTH / 2 + r, WIDTH / 2 - r)
        y = uniform(-HEIGHT / 2 + r, HEIGHT / 2 - r)
        m = turtle.Turtle()
        m.shape("circle")
        m.shapesize(size)
        m.penup()
        m.goto(x, y)
        v = uniform(MIN_V, MAX_V)
        angle = uniform(0, 2 * math.pi)
        return Ball(m, v * math.cos(angle), v * math.sin(angle), r)


def balls_collide(b1, b2):
    d = math.sqrt((b1.m.xcor() - b2.m.xcor()) ** 2 + (b1.m.ycor() - b2.m.ycor()) ** 2)
    return d <= b1.r + b2.r


def process_collision(b1, b2):
    a = math.atan2(b2.m.ycor() - b1.m.ycor(), b2.m.xcor() - b1.m.xcor())
    A1n = math.atan2(b1.vy, b1.vx) - a
    A2n = math.atan2(b2.vy, b2.vx) - a

    v1 = math.sqrt(b1.vx**2 + b1.vy**2)
    v2 = math.sqrt(b2.vx**2 + b2.vy**2)

    vr1 = v1 * math.cos(A1n)
    vt1 = v1 * math.sin(A1n)

    vr2 = v2 * math.cos(A2n)
    vt2 = v2 * math.sin(A2n)

    m1, m2 = b1.mass(), b2.mass()
    vr1n = (vr1 * (m1 - m2) + 2 * m2 * vr2) / (m1 + m2)
    vr2n = vr1 + vr1n - vr2

    v1n = math.sqrt(vr1n**2 + vt1**2)
    v2n = math.sqrt(vr2n**2 + vt2**2)

    A1nn = math.atan2(vt1, vr1n) + a
    A2nn = math.atan2(vt2, vr2n) + a

    b1.vx = v1n * math.cos(A1nn)
    b1.vy = v1n * math.sin(A1nn)

    b2.vx = v2n * math.cos(A2nn)
    b2.vy = v2n * math.sin(A2nn)


sim_state = SimState.setup()
setup_screen("Minigolf")
# draw_vessel()

ball = turtle.Turtle()
ball.goto(50, 100)
ball.radians()
ball.setheading(10)
ballVelocity = 10  # 5


def wall_hit(w):  # , out float alpha)
    ballX = ball.xcor()
    ballY = ball.ycor()
    ballRadius = 10  # 5

    a = math.sqrt((ballX - w.x1) * (ballX - w.x1) + (ballY - w.y1) * (ballY - w.y1))
    b = math.sqrt((ballX - w.x2) * (ballX - w.x2) + (ballY - w.y2) * (ballY - w.y2))
    c = math.sqrt((w.x1 - w.x2) * (w.x1 - w.x2) + (w.y1 - w.y2) * (w.y1 - w.y2))

    P = (a + b + c) / 2
    h = 2 * math.sqrt(P * (P - a) * (P - b) * (P - c)) / c

    m = math.sqrt(a * a - h * h)
    n = math.sqrt(b * b - h * h)

    alpha = 0

    if n + m - c < 0.01 and h < ballRadius:
        alpha = math.pi / 2 + math.atan2(w.y2 - w.y1, w.x2 - w.x1)
        print(f"b1: {alpha}")
        return alpha

    if a < ballRadius or b < ballRadius:
        wx = w.x1 if (a < ballRadius) else w.x2
        wy = w.y1 if (a < ballRadius) else w.y2
        alpha = math.atan2(wy - ballY, wx - ballX)
        print(f"b2: ")
        return alpha

    return None


def do_collision(w):
    # float alpha;
    # ballVelocity = 0
    if alpha := wall_hit(w) is not None:
        # ball.left()
        # ball
        ballAngle = ball.heading()
        ballAngle -= alpha
        ballAngle = math.atan2(
            ballVelocity * math.sin(ballAngle), -ballVelocity * math.cos(ballAngle)
        )

        ballAngle += alpha
        ball.setheading(ballAngle)


@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float


# 50 100 0
walls = [
    Wall(400, 115, 400, 300),
    Wall(200, 150, 300, 300),
    Wall(0, 0, 500, 0),
    Wall(0, 0, 0, 400),
    Wall(0, 400, 500, 400),
    Wall(500, 400, 500, 0),
]
# ball = Ball.create()
# b2 = Ball.create()

t = turtle.Turtle()
for w in walls:
    t.penup()
    t.goto(w.x1, w.y1)
    t.pendown()
    t.goto(w.x2, w.y2)


def tick():
    if not sim_state.done:
        ball.forward(ballVelocity)

        for w in walls:
            do_collision(w)
        # if balls_collide(ball, b2):
        #     process_collision(ball, b2)

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
