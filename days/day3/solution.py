import re


class bcolors:
    yes = "\033[92m"
    no = "\033[91m"
    ENDC = "\033[0m"


FNAME = "./inp.txt"

rgx_do = re.compile(r"do\(\)")
rgx_dont = re.compile(r"don\'t\(\)")
rgx = re.compile(r"mul\(\d{,3},\d{,3}\)")

with open(FNAME, "r") as f:
    data = f.read()

res = 0
dos = set([o.start() for o in rgx_do.finditer(data)])
donts = set([p.start() for p in rgx_dont.finditer(data)])

# I later realized, that I don't need to do any mask and
# I just can do one regexp, but it's too late, I keep the mask
allowed = True
mask = []
for i in range(len(data)):
    if i in donts:
        allowed = False
    if i in dos:
        allowed = True
    mask.append(allowed)

for idx, c in enumerate(data):
    col = bcolors.yes if mask[idx] else bcolors.no
    print(f"{col}{c}{bcolors.ENDC}", end="")
print()

matches = rgx.finditer(data)
for m in matches:
    pos = m.start()
    if not mask[pos]:
        continue
    s = m.group()
    a, b = s.split(",", 1)
    a = int(a[4:])
    b = int(b[: len(b) - 1])
    res += a * b

print(res)
