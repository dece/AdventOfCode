from intcode import Intcode, AIC


def main():
    codes = Intcode.parse_file("day25.txt")
    dr = DroidRemote(codes)
    dr.run()


class DroidRemote(AIC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_text = ""
    
    def input_data(self):
        if not self.input_text:
            self.input_text = self.keybind(input(">")) + "\n"
        return super().input_data()

    def keybind(self, s):
        return {
            "i": "inv",
            "n": "north",
            "e": "east",
            "s": "south",
            "w": "west",
        }.get(s, s)


if __name__ == "__main__":
    main()
