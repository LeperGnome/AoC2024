from functools import cache

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

stones = [int(s) for s in data.split(" ")]

def apply_rule(s: int) -> list[int]:
    if s == 0:
        return [1]
    ss = str(s)
    if len(ss) % 2 == 0:
        return [int(ss[:len(ss)//2]), int(ss[len(ss)//2:])]
    return [s*2024]

it = 75

@cache
def get_cnt(s: int, left: int) -> int:
    if left == 0:
        return 1
    cnt = 0
    for ns in apply_rule(s):
        cnt += get_cnt(ns, left-1)
    return cnt

print(sum(get_cnt(s, it) for s in stones))
