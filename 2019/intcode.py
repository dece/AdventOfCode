""" Intcode interpreter. Day 11. """

from enum import IntEnum
import sys


class Op(IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JNZ = 5
    JEZ = 6
    LT = 7
    EQ = 8
    SRB = 9
    HALT = 99


class PMode(IntEnum):
    POS = 0
    IMM = 1
    REL = 2


class Intcode(object):

    def __init__(self, program, debug=False):
        self._memory = program.copy()
        self.ip = 0
        self.rel_base = 0
        self.ctx_op = None
        self.ctx_modes = None
        self.halt = False
        self.inputs = None
        self.debug = debug

    @staticmethod
    def parse_input(text):
        return [int(i) for i in text.rstrip().split(",")]
    
    def log(self, message, *args):
        if self.debug:
            print("debug:", message, *args)
    
    def run(self, inputs=None):
        self.inputs = inputs or []
        handlers = self.get_handlers()
        while not self.halt:
            self.read_code()
            handlers.get(self.ctx_op)()

    def get_handlers(self):
        return {
            Op.ADD: self.op_add,
            Op.MUL: self.op_mul,
            Op.IN: self.op_in,
            Op.OUT: self.op_out,
            Op.JNZ: self.op_jnz,
            Op.JEZ: self.op_jez,
            Op.LT: self.op_lt,
            Op.EQ: self.op_eq,
            Op.SRB: self.op_srb,
            Op.HALT: self.op_halt,
        }

    def mem_get(self, pos):
        self._check_memory_limits(pos)
        return self._memory[pos]
    
    def mem_set(self, pos, value):
        self._check_memory_limits(pos)
        self._memory[pos] = value

    def _check_memory_limits(self, index):
        if index >= len(self._memory):
            new_size = index + 1
            self._memory += [0] * (new_size - len(self._memory))

    def read_code(self):
        raw_code = self.mem_get(self.ip)
        code = raw_code % 100
        self.ctx_op = Op(code)

        code = raw_code // 100
        self.ctx_modes = []
        for _ in range(0, 3):
            self.ctx_modes.append(PMode(code % 10))
            code //= 10
        self.log("read_code", raw_code, self.ctx_op, self.ctx_modes)

    def param(self, index, pointer=False):
        mode = self.ctx_modes[index - 1]
        if mode == PMode.POS:
            address = self.mem_get(self.ip + index)
            return address if pointer else self.mem_get(address)
        elif mode == PMode.IMM:
            return self.mem_get(self.ip + index)
        elif mode == PMode.REL:
            address = self.rel_base + self.mem_get(self.ip + index)
            return address if pointer else self.mem_get(address)
    
    def write_at_param(self, param_offset, value):
        self.mem_set(self.param(param_offset, pointer=True), value)

    def op_add(self):
        self.write_at_param(3, self.param(1) + self.param(2))
        self.ip += 4

    def op_mul(self):
        self.write_at_param(3, self.param(1) * self.param(2))
        self.ip += 4

    def op_in(self):
        self.mem_set(self.param(1, pointer=True), self.input_data())
        self.ip += 2

    def op_out(self):
        self.output_data(self.param(1))
        self.ip += 2

    def op_jnz(self):
        if self.param(1) != 0:
            self.ip = self.param(2)
        else:
            self.ip += 3

    def op_jez(self):
        if self.param(1) == 0:
            self.ip = self.param(2)
        else:
            self.ip += 3

    def op_lt(self):
        self.write_at_param(3, int(self.param(1) < self.param(2)))
        self.ip += 4

    def op_eq(self):
        self.write_at_param(3, int(self.param(1) == self.param(2)))
        self.ip += 4

    def op_srb(self):
        self.rel_base += self.param(1)
        self.ip += 2

    def op_halt(self):
        self.halt = True

    def input_data(self):
        return self.inputs.pop(0)
    
    def output_data(self, data):
        print(">", data)
