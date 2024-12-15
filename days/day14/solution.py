from io import StringIO
from collections import defaultdict
from dataclasses import dataclass
from contextlib import contextmanager

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int


@contextmanager
def alt_buffer():
    try:
        print("\033[?1049h\033[22;0;0t\033[0;0H", end="")
        yield
    finally:
        print("\033[?1049l\033[23;0;0t", end="")


seconds = 100

maxx = 101
maxy = 103

xcenter = maxx // 2
ycenter = maxy // 2

robots: list[Robot] = []
m = defaultdict(int)

for line in data.splitlines(False):
    coords, vel = line.split(" ")
    x, y = coords.split("=")[1].split(",", 1)
    vx, vy = vel.split("=")[1].split(",", 1)
    robots.append(Robot(x=int(x), y=int(y), vx=int(vx), vy=int(vy)))
    m[(x, y)] += 1


def print_robots() -> str:
    s = StringIO()
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if m[(x, y)] > 0:
                print("#", end="", file=s)
            else:
                print(".", end="", file=s)
        print(file=s)
    s.seek(0)
    return s.read()


i = 0
while True:
    i += 1
    for r in robots:
        m[(r.x, r.y)] -= 1

        r.x = (r.x + r.vx) % maxx
        r.y = (r.y + r.vy) % maxy

        m[(r.x, r.y)] += 1

    s = print_robots()
    # might be naive, but it works =)
    if "##############" in s:
        with alt_buffer():
            print(s)
            print(i)
            input()
            print(chr(27) + "[2J")
