from itertools import product
import operator

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read()


def concat(x: int, y: int) -> int:
    return int(str(x) + str(y))


s = 0
lines = data.splitlines(keepends=False)
for line in lines:
    t, nums = line.split(": ", 1)
    t = int(t)
    nums = list(map(int, nums.split(" ")))
    for opers in product([concat, operator.mul, operator.add], repeat=len(nums) - 1):
        r = nums[0]
        for n, oper in zip(nums[1:], opers):
            r = oper(r, n)
            if r > t:
                break
        if r == t:
            s += t
            break

print(s)
