""" Intcode interpreter. Day 9. """

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

    def __init__(self, program, print_output=False):
        self._memory = program.copy()
        self.ip = 0
        self.rel_base = 0
        self.inputs = []
        self.ctx_op = None
        self.ctx_modes = None
        self.halt = False
        self.outputs = []
        self.print_output = print_output

    @staticmethod
    def parse_input(text):
        return [int(i) for i in text.rstrip().split(",")]
    
    def run(self, inputs=None):
        self.inputs = inputs or []
        handlers = self.get_handlers()
        while not self.halt:
            self.read_code()
            handler = handlers.get(self.ctx_op)
            if not handler:
                sys.exit("Wrong opcode: {}".format(self.ctx_op))
            try:
                handler()
            except Exception as exc:
                sys.exit("Exception: {}".format(exc))
        return self.outputs[-1] if self.outputs else 0

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
            self._extend_memory(index + 1)

    def _extend_memory(self, new_size):
        if len(self._memory) >= new_size:
            return
        self._memory += [0] * (new_size - len(self._memory))

    def read_code(self):
        code = self.mem_get(self.ip)
        self.ctx_op = code % 100
        code //= 100
        self.ctx_modes = []
        for _ in range(0, 3):
            self.ctx_modes.append(PMode(code % 10))
            code //= 10

    def param(self, index):
        mode = self.ctx_modes[index - 1]
        if mode == PMode.POS:
            address = self.mem_get(self.ip + index)
            return self.mem_get(address)
        elif mode == PMode.IMM:
            return self.mem_get(self.ip + index)
        elif mode == PMode.REL:
            relative_jump = self.mem_get(self.ip + index)
            address = self.rel_base + relative_jump
            return self.mem_get(address)
    
    def write_pos_ofs(self, pos_offset, value):
        output_pos = self.mem_get(self.ip + pos_offset)
        self.mem_set(output_pos, value)
    
    def op_add(self):
        self.write_pos_ofs(3, self.param(1) + self.param(2))
        self.ip += 4

    def op_mul(self):
        self.write_pos_ofs(3, self.param(1) * self.param(2))
        self.ip += 4

    def op_in(self):
        self.write_pos_ofs(1, self.inputs.pop(0))
        self.ip += 2

    def op_out(self):
        self.outputs.append(self.param(1))
        if self.print_output:
            print(">", self.outputs[-1])
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
        self.write_pos_ofs(3, int(self.param(1) < self.param(2)))
        self.ip += 4

    def op_eq(self):
        self.write_pos_ofs(3, int(self.param(1) == self.param(2)))
        self.ip += 4

    def op_srb(self):
        self.rel_base += self.param(1)
        self.ip += 2

    def op_halt(self):
        self.halt = True
