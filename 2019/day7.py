import itertools
from queue import Queue
from threading import Thread

from intcode import Intcode


def main():
    with open("day7.txt", "rt") as input_file:
        first_line = input_file.readlines()[0]
    codes = Intcode.parse_input(first_line)

    # Part 1
    phase_settings_perm = itertools.permutations(range(5), 5)
    max_output = 0
    for phases in phase_settings_perm:
        inout = 0
        for amp_id in range(5):
            amp = Amp(codes)
            amp.run([phases[amp_id], inout])
            inout = amp.output_queue.get()
        max_output = max(max_output, inout)
    print("Max output:", max_output)

    # Part 2
    phase_settings_perm = itertools.permutations(range(5, 10), 5)
    max_output = 0
    for phases in phase_settings_perm:
        inout = 0
        amps = [Amp(codes) for _ in range(5)]
        threads = []
        for amp_id, amp in enumerate(amps):
            parent_index = (amp_id - 1) % 5
            amp.parent = amps[parent_index]
            args = [[phases[amp_id]]]
            if amp_id == 0:
                args[0].append(0)
            threads.append(Thread(target=amp.run, args=args))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        inout = amp.output_queue.get()
        max_output = max(max_output, inout)
    print("Max output chained:", max_output)


class Amp(Intcode):

    def __init__(self, codes):
        super().__init__(codes)
        self.parent = None
        self.output_queue = Queue()

    def input_data(self):
        if self.inputs:
            return self.inputs.pop(0)
        return self.parent.output_queue.get()

    def output_data(self, data):
        self.output_queue.put(data)


if __name__ == "__main__":
    main()
