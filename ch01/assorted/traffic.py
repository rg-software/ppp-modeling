import turtle
import math
from random import uniform, randint
from dataclasses import dataclass

WIDTH = 600
HEIGHT = 400
MARGIN = 50
SLEEP_MS = 20
R = 200
EPSILON = 0.0001

N = 25
MIN_SPEED = 4
MAX_SPEED = 7
SAFE_DISTANCE_STEPS = 15
CRASH_DISTANCE = 2
DECEL = 0.4
ACCEL = 0.1
REACTION_TIME = 15
DISRUPTION_TIME = 70


@dataclass
class SimState:
    done: bool
    cars: list

    def set_done(self):
        self.done = True

    def gen_disruption(self):
        self.cars[randint(0, N - 1)].disrupt()

    @classmethod
    def setup(cls, cars):
        r = cls(False, cars)
        turtle.listen()
        turtle.onkeypress(r.set_done, "space")
        turtle.onkeypress(r.gen_disruption, "Return")
        return r


@dataclass
class Car:
    m: turtle.Turtle
    angle: float
    pref_speed: float
    speed: float
    front_car: object = None
    in_disrupt: bool = False
    pause_steps: int = 0

    def disrupt(self):
        self.in_disrupt = True

    def accelerate(self):
        if self.pause_steps > 0:
            self.pause_steps -= 1
        else:
            self.speed = min(self.pref_speed, self.speed + ACCEL)

    def decelerate(self):
        self.speed = max(0, self.speed - DECEL)
        if self.speed == 0:
            self.pause_steps = DISRUPTION_TIME if self.in_disrupt else REACTION_TIME
            self.in_disrupt = False

    def front_distanace(self):
        angle = self.front_car.angle - self.angle
        return R * (angle if angle >= 0 else angle + 2 * math.pi)

    def front_distance_steps(self):
        return self.front_distanace() / (self.speed + EPSILON)

    def adjust_speed(self):
        if self.front_distanace() < CRASH_DISTANCE:
            print("Crash!")
            sim_state.set_done()
        elif self.front_distance_steps() < SAFE_DISTANCE_STEPS or self.in_disrupt:
            self.decelerate()
        elif self.speed < self.pref_speed:
            self.accelerate()

    def move(self):
        self.adjust_speed()
        self.angle += self.speed / R
        self.m.goto(R * math.cos(self.angle), R * math.sin(self.angle))

    @classmethod
    def create(cls, angle):
        m = turtle.Turtle()
        m.shape("circle")
        m.shapesize(0.2)
        m.penup()
        speed = uniform(MIN_SPEED, MAX_SPEED)
        return cls(m, angle, speed, speed)


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


def setup_cars():
    cars = [Car.create(i * 2 * math.pi / N) for i in range(N)]
    for i in range(N):
        cars[i].front_car = cars[(i + 1) % N]
    return cars


setup_screen("Traffic shockwaves")
cars = setup_cars()
sim_state = SimState.setup(cars)


def tick():
    if not sim_state.done:
        for c in cars:
            c.move()

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
