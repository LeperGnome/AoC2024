FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read()

print(data)
lines = data.splitlines(keepends=False)
CHARS: list[list[str]] = [list(l) for l in lines]


def get_str(init: tuple[int, int], offsets: list[tuple[int, int]]) -> str:
    comb = []
    ridx, cidx = init
    for rdx, cdx in offsets:
        if 0 <= ridx + rdx <= len(CHARS) - 1 and 0 <= cidx + cdx <= len(CHARS[0]) - 1:
            comb.append(CHARS[ridx + rdx][cidx + cdx])
    return "".join(comb)


def nxmas(ridx, cidx) -> int:
    res = 0
    # Pt. 1
    # dirs = [
    #     [(0,0), (0,1), (0,2), (0,3)],  # horizontal
    #     [(0,0), (1,0), (2,0), (3,0)],  # vertical
    #     [(0,0), (1,1), (2,2), (3,3)],  # diag right down
    #     [(0,0), (-1,1), (-2,2), (-3,3)],  # diag right up
    # ]

    dir = [
        (0, 0),
        (0, 2),
        (1, 1),
        (2, 0),
        (2, 2),
    ]
    s = get_str((ridx, cidx), dir)

    """
    M.S   S.S   M.M   S.M
    .A.   .A.   .A.   .A.
    M.S   M.M   S.S   S.M
                      
    MSAMS SSAMM MMASS SMASM
    """
    if s in [
        "MSAMS",
        "SSAMM",
        "MMASS",
        "SMASM",
    ]:
        res += 1
    return res
