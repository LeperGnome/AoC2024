import numpy as np


FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

systems = []

secs = data.split("\n\n")

for sec in secs:
    lines = sec.splitlines(False)
    x0 = int(lines[0].split(" ")[2][2:-1])
    y0 = int(lines[0].split(" ")[3][2:])

    x1 = int(lines[1].split(" ")[2][2:-1])
    y1 = int(lines[1].split(" ")[3][2:])

    c0 = 10000000000000 + int(lines[2].split(" ")[1][2:-1])
    c1 = 10000000000000 + int(lines[2].split(" ")[2][2:])

    systems.append([[[x0, x1], [y0, y1]], [c0, c1]])

s = 0
for a, b in systems:
    t1, t2 = np.linalg.solve(np.array(a), np.array(b))
    if any(0.0001 < x % 1 < 0.9999 for x in (t1, t2)):
        continue
    s += t1 * 3 + t2


print(int(s))
