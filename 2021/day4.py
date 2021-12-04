import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]
    pack = list(map(int, lines[0].split(",")))
    boards = []
    for i in range(2, len(lines), 6):
        boards.append([
            list(map(int, filter(bool, line.split())))
            for line in lines[i:i+5]
        ])

    # Part 1
    find_winner(boards, pack)

    # Part 2
    not_won_yet = [1] * len(boards)
    iterpack = iter(pack)  # just so we can avoid looping twice
    for n in iterpack:
        for b, board in enumerate(boards):
            board_marked = False
            for x, row in enumerate(board):
                for y, num in enumerate(row):
                    if num == n:
                        board[x][y] = -1
                        board_marked = True
                        break
                if board_marked:
                    break
            if get_unmarked_sum_if_winning(board) is not None:
                not_won_yet[b] = 0
        if sum(not_won_yet) == 1:
            print("We have a loser...")
            ib = not_won_yet.index(1)
            find_winner([boards[ib]], iterpack)
            break


def find_winner(boards, pack):
    won = False
    for n in pack:
        for board in boards:
            board_marked = False
            for x, row in enumerate(board):
                for y, num in enumerate(row):
                    if num == n:
                        board[x][y] = -1
                        board_marked = True
                        break
                if board_marked:
                    break
            if unmarked_sum := get_unmarked_sum_if_winning(board):
                score = unmarked_sum * n
                print("We have a winner!", score)
                won = True
                break
        if won:
            break


def get_unmarked_sum_if_winning(board):
    for row in board:
        if row == [-1, -1, -1, -1, -1]:
            return get_unmarked_sum(board)
    for col in range(len(board)):
        if all(row[col] == -1 for row in board):
            return get_unmarked_sum(board)
    return None


def get_unmarked_sum(board):
    return sum(n for row in board for n in row if n != -1)


if __name__ == "__main__":
    main()
