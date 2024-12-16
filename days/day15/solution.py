FNAME = "./inp.txt"
Point = tuple[int, int]

with open(FNAME, "r") as f:
    data = f.read().strip()

m, r = data.split("\n\n", 1)

m = m.replace("#", "##")
m = m.replace(".", "..")
m = m.replace("O", "[]")
m = m.replace("@", "@.")

MAP: list[list[str]] = [list(r) for r in m.splitlines(False)]
max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1

dirm: dict[str, Point] = {
    "v": (1, 0),
    ">": (0, 1),
    "^": (-1, 0),
    "<": (0, -1),
}

dirs = "".join(r.splitlines(False))


def get_coords(c: str) -> list[Point]:
    res = []
    for ri, row in enumerate(MAP):
        for ci, col in enumerate(row):
            if col == c:
                res.append((ri, ci))
    return res


def add_points(p1: Point, p2: Point):
    return (p1[0] + p2[0], p1[1] + p2[1])


def within_map(p: Point) -> bool:
    return 0 <= p[0] <= max_row and 0 <= p[1] <= max_col


robot: Point = get_coords("@")[0]

# storing only left edges
boxes: set[Point] = set(get_coords("["))


def print_map():
    for (
        ri,
        row,
    ) in enumerate(MAP):
        for ci, col in enumerate(row):
            p = (ri, ci)
            b = which_box(p)
            if p == b:
                print("[", end="")
            elif left_to(p) == b:
                print("]", end="")
            elif p == robot:
                print("@", end="")
            elif col == "#":
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def left_to(p: Point) -> Point:
    return (p[0], p[1] - 1)


def right_to(p: Point) -> Point:
    return (p[0], p[1] + 1)


def which_box(p: Point) -> Point | None:
    # p is left edge, so returning it
    if p in boxes:
        return p

    lp = left_to(p)

    # p is right edge, so returning left, since we store only left edges
    if lp in boxes:
        return lp

    # not a box
    return None


def is_wall(p) -> bool:
    return MAP[p[0]][p[1]] == "#"


for ds in dirs:
    dir = dirm[ds]

    boxes_to_move = []
    hit_a_wall = False

    nextpts = [add_points(robot, dir)]

    while nextpts and all(within_map(p) for p in nextpts):
        if any(is_wall(p) for p in nextpts):
            hit_a_wall = True
            break

        hit_a_box = False

        # preparing next "next points"
        nnpts = []
        for p in nextpts:
            if b := which_box(p):
                boxes_to_move.append(b)
                # going right -> checking point next to box right edge
                if dir[1] == 1:
                    nnpts.append(add_points(right_to(b), dir))

                # going left -> checking point next to box right edge
                elif dir[1] == -1:
                    nnpts.append(add_points(b, dir))

                # if doing any vertical movement, checking adjacent
                # points to left and right edge of the box
                if dir[0] != 0:
                    nnpts += [add_points(b, dir), add_points(right_to(b), dir)]
                hit_a_box = True
        # checking points, adjacent ot all boxes we hit
        if hit_a_box:
            nextpts = nnpts
        # did not hit any walls and already counted all touched boxes,
        # so no next points to check further
        else:
            nextpts = []
    else:
        robot = add_points(robot, dir)
        for b in reversed(boxes_to_move):
            if b in boxes:
                boxes.remove(b)
                boxes.add(add_points(b, dir))

res = 0
for b in boxes:
    res += 100 * b[0] + b[1]


print_map()
print(res)
