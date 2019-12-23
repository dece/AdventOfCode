from queue import Empty, SimpleQueue
from threading import Thread
import time

from intcode import Intcode


def main():
    codes = Intcode.parse_file("day23.txt")
    network = Network(50, codes)

    # Part 1
    for nic in network.nics:
        thread = Thread(target=lambda: nic.run(), name=f"NIC {nic.address}")
        thread.start()
    
    # Part 2
    last_nat_y = None
    while True:
        time.sleep(0.1)
        for nic in network.nics:
            if not nic.inq.empty:
                break
        else:
            if not network.last_nat_packet:
                continue
            x, y = network.last_nat_packet
            if y == last_nat_y:
                exit(f"Sending another {y} from NAT.")
            last_nat_y = y
            print(f"Network is idle, sending NAT packet to 0.")
            network.nics[0].inq.put(x)
            network.nics[0].inq.put(y)


class Network:

    def __init__(self, size, codes):
        self.nics = [NIC(address, self, codes) for address in range(size)]
        self.last_nat_packet = None

    def route(self, sender, dest, x, y):
        if dest == 255:
            print(f"NAT: {x, y}.")
            self.last_nat_packet = (x, y)
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
