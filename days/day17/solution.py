from typing import Callable


FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()


Instruction = Callable[[int], None]


class Processor:
    rA: int
    rB: int
    rC: int

    prog: list[int]
    stdout: list[int]

    _cnt: int
    _imap: dict[int, Instruction]

    def __init__(self, rA: int, rB: int, rC: int, prog: list[int]):
        self.rA = rA
        self.rB = rB
        self.rC = rC
        self.prog = prog
        self.stdout = []
        self._cnt = 0
        self._imap = {
            0: self._adv,
            1: self._bxl,
            2: self._bst,
            3: self._jnz,
            4: self._bxc,
            5: self._out,
            6: self._bdv,
            7: self._cdv,
        }

    def _combo_op_to_value(self, op: int) -> int:
        if 0 <= op <= 3:
            return op
        if op == 4:
            return self.rA
        if op == 5:
            return self.rB
        if op == 6:
            return self.rC
        else:
            raise RuntimeError("invalid combo operand")

    def _adv(self, op: int):
        self.rA = self.rA // (2 ** self._combo_op_to_value(op))
        self._cnt += 2

    def _bxl(self, op: int):
        self.rB ^= op
        self._cnt += 2

    def _bst(self, op: int):
        self.rB = self._combo_op_to_value(op) % 8
        self._cnt += 2

    def _jnz(self, op: int):
        if self.rA == 0:
            self._cnt += 2
            return
        self._cnt = op

    def _bxc(self, _: int):
        self.rB ^= self.rC
        self._cnt += 2

    def _out(self, op: int):
        self.stdout.append(self._combo_op_to_value(op) % 8)
        self._cnt += 2

    def _bdv(self, op: int):
        self.rB = self.rA // (2 ** self._combo_op_to_value(op))
        self._cnt += 2

    def _cdv(self, op: int):
        self.rC = self.rA // (2 ** self._combo_op_to_value(op))
        self._cnt += 2

    def _get_instruction_method(self, code: int) -> Instruction:
        return self._imap[code]

    def step(self) -> bool:
        if not 0 <= self._cnt < len(self.prog):
            return False

        inst = self._get_instruction_method(self.prog[self._cnt])
        op = self.prog[self._cnt + 1]

        inst(op)
        return True

    def run(self) -> str:
        while 0 <= self._cnt < len(self.prog):
            # print(f"{self.rA=}", f"{self.rB=}", f"{self.rC=}", sep="\n")
            # print(self._stdout)
            # print(*self.prog)
            # print(*[
            #     "^" if idx == self._cnt else " "
            #     for idx, _ in enumerate(self.prog)
            # ])

            inst = self._get_instruction_method(self.prog[self._cnt])
            op = self.prog[self._cnt + 1]

            # print(inst.__name__, op)
            # input()

            inst(op)

        return ",".join([str(x) for x in self.stdout])


r, prog = data.split("\n\n")
regs = []
for i in r.splitlines(False):
    regs.append(int(i.split(": ", 1)[1]))

a, b, c = regs
prog = [int(i) for i in prog.split(": ", 1)[1].split(",")]


# --- manual approach


def alg(a, b=0, c=0):
    out = []
    while True:
        b = (a & 7) ^ 3
        c = a >> b
        b ^= 5 ^ c
        a >>= 3
        out.append(b & 7)
        if a == 0:
            break
    return out


def find_quine(prog: list[int], start: int, a: int) -> int:
    res = set()

    for i in range(8):
        acc = (a << 3) + i
        out = alg(acc)
        print(acc, out)
        if out == prog[start:]:
            if out == prog:
                res.add(acc)
            else:
                # this gives me the ability to back-track unsuccessfull 'a'
                na = find_quine(prog, start - 1, acc)
                if na:
                    res.add(na)
    if res:
        return min(res)
    return 0


print(find_quine(prog, len(prog) - 1, 0))

# --- brute force didn't work ---
#
# def calc(n: int, start:int, step: int, prog: list[int]):
#     a = start
#     while True:
#         print(a)
#         proc = Processor(a, b, c, prog)
#         while proc.step():
#             if len(proc.stdout) > 7:
#                 print(proc.rA, proc.rB, proc.rC)
#                 print(proc.stdout)
#             if proc.stdout != prog[:len(proc.stdout)]:
#                 break
#         else:
#             if proc.stdout == prog:
#                 break
#         a *= 8
#     print(f"{n} res: {a}")
#     sys.exit()
#
# if __name__ == "__main__":
#     # s = 627500000
#     # s = 2867000000
#     s = 1
#     # s = 0
#     nproc = 1
#     workers = []
#
#     ctx = mp.get_context('spawn')
#
#     for w in range(nproc):
#         args = (w, s+w, nproc, deepcopy(prog),)
#         p = ctx.Process(target=calc, args=args)
#         p.start()
#         workers.append(p)
#
#     for w in workers[::-1]:
#         w.join()
#
# --- not really working ---
