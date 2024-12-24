from functools import cache

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

towels, designs = data.split("\n\n")

towels = tuple(towels.split(", "))
designs = designs.splitlines(False)

@cache
def count_designs(towels, design):
    if design == "":
        return 1

    result = 0
    for towel in towels:
        if towel == design[:len(towel)]:
            result += count_designs(
                towels,
                design[len(towel):],
            )

    return result

res = {
    d : count_designs(towels, d) 
    for d in designs
}

print(f'Part 1: {len([1 for v in res.values() if v >= 1])}')
print(f'Part 2: {sum(res.values())}')
