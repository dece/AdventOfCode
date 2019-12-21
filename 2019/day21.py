import sys

from intcode import AIC


def main():
    codes = AIC.parse_file("day21.txt")
    ss = SSIC(codes, script=sys.stdin.read())
    ss.run()


class SSIC(AIC):

    def __init__(self, *args, script="", **kwargs):
        super().__init__(*args, **kwargs)
        self.input_text = script


if __name__ == "__main__":
    main()
