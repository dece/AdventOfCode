def main():
    with open("day8.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]

    # Part 1
    visited = set()
    vm = Vm(lines)
    while vm.ip not in visited:
        visited.add(vm.ip)
        vm.step()
    print("Acc after revisiting op:", vm.acc)

    # Part 2
    jmps = reversed([i for i, inst in enumerate(vm.code) if inst[0] == "jmp"])
    for i in jmps:
        vm.reset()
        orig_jmp = vm.code[i]
        vm.code[i] = ["nop", orig_jmp[1]]
        if not vm.does_loop():
            print(vm.acc)
            return
    # No need to try for nops apparently!

        
class Vm:

    def __init__(self, code):
        self.text = code
        self.reset()

    def reset(self):
        self.code = self.parse_code(self.text)
        self.ip = 0
        self.acc = 0

    def step(self):
        inst = self.code[self.ip]
        if inst[0] == "nop":
            pass
        elif inst[0] == "jmp":
            self.ip += int(inst[1])
            return
        elif inst[0] == "acc":
            self.acc += int(inst[1])
        self.ip += 1

    def does_loop(self):
        visited = set()
        while self.ip < len(self.code):
            visited.add(self.ip)
            self.step()
            if self.ip in visited:
                return True
        return False

    @staticmethod
    def parse_code(code):
        ops = []
        for line in code:
            ops.append(line.split())
        return ops


if __name__ == "__main__":
    main()
