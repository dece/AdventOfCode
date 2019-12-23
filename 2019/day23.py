from queue import Empty, SimpleQueue
from threading import Thread

from intcode import Intcode


def main():
    codes = Intcode.parse_file("day23.txt")
    network = Network(50, codes)
    for nic in network.nics:
        thread = Thread(target=lambda: nic.run(), name=f"NIC {nic.address}")
        thread.start()


class Network:

    def __init__(self, size, codes):
        self.nics = [NIC(address, self, codes) for address in range(size)]

    def route(self, sender, dest, x, y):
        if dest == 255:
            print(f"Packet to 255: {x, y}.")
            return
        print(f"Send {x, y} from {sender} to {dest}")
        self.nics[dest].inq.put(x)
        self.nics[dest].inq.put(y)


class NIC(Intcode):

    def __init__(self, address, network, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = address
        self.network = network
        self.inq = SimpleQueue()
        self.inq.put(address)
        self.outq = []

    def input_data(self):
        try:
            data = self.inq.get(timeout=0.1)
        except Empty:
            data = -1
        return data

    def output_data(self, data):
        self.outq.append(data)
        if len(self.outq) == 3:
            self.network.route(self.address, *self.outq)
            self.outq = []
            return


if __name__ == "__main__":
    main()
