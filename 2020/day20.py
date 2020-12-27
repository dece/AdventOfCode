import math
import sys

DIM = 10

def main():
    groups = sys.stdin.read().rstrip().split("\n\n")
    tiles = {}
    for group in groups:
        lines = [line.rstrip() for line in group.splitlines()]
        tile_id = int(lines[0][5:].rstrip(":"))
        tiles[tile_id] = list(map(list, lines[1:]))
    idim = int(math.sqrt(len(tiles)))

    # Part 1
    # instructions are not very clean, but looks like we only have to check 3
    # rotations + optionally horizontal flip. vertical flip is not needed on
    # example, and a vflip is actually rot180 + hflip.
    perms = {}
    for tile_id, tile in tiles.items():
        perms[tile_id] = permutations(tile)
    image = search({}, 0, 0, [], perms, idim)
    tl = image[(0, 0)]
    tr = image[(0, idim - 1)]
    bl = image[(idim - 1, 0)]
    br = image[(idim - 1, idim - 1)]
    print("Multiplied corners:", tl[0] * tr[0] * bl[0] * br[0])

    # Part 2
    pattern = [
        (0, 0), (1, 1),
        (4, 1), (5, 0), (6, 0), (7, 1),
        (10, 1), (11, 0), (12, 0), (13, 1),
        (16, 1), (17, 0), (18, 0), (18, -1), (19, 0)
    ]
    merged = merge_tiles(image, perms, idim)
    global DIM
    DIM = len(merged)
    perms = permutations(merged)
    max_monsters = max(find_monsters(perm, pattern) for perm in perms)
    num_dashes = sum(c == "#" for row in merged for c in row)
    monster_dashes = max_monsters * len(pattern)
    print("Roughness:", num_dashes - monster_dashes)

def permutations(tile):
    return [
        tile,
        hflip(tile),
        rot90(tile),
        rot90(hflip(tile)),
        rot90(rot90(tile)),
        rot90(rot90(hflip(tile))),
        rot90(rot90(rot90(tile))),
        rot90(rot90(rot90(hflip(tile)))),
    ]

def rot90(tile):
    rtile = [[None for _ in range(DIM)] for _ in range(DIM)]
    for x in range(DIM):
        for y in range(DIM):
            rtile[x][y] = tile[DIM - y - 1][x]
    return rtile

def hflip(tile):
    return [row[::] for row in tile[::-1]]

def search(image, x, y, placed, perms, idim):
    fitting = find_fitting(image, x, y, placed, perms)
    if (x, y) == (idim - 1, idim - 1) and len(fitting) == 1:
        image[(idim - 1, idim - 1)] = fitting[0]
        return image
    for fit in fitting:
        nimage = image.copy()
        nimage[(x, y)] = fit
        nx = (x + 1) % idim
        ny = y if nx > 0 else y + 1
        nplaced = placed + [fit[0]]
        if (complete_image := search(nimage, nx, ny, nplaced, perms, idim)):
            return complete_image

def find_fitting(image, x, y, placed, perms):
    up_perm = image.get((x, y - 1))
    up = perms[up_perm[0]][up_perm[1]] if up_perm else None
    left_perm = image.get((x - 1, y))
    left = perms[left_perm[0]][left_perm[1]] if left_perm else None
    down_perm = image.get((x, y + 1))
    down = perms[down_perm[0]][down_perm[1]] if down_perm else None
    right_perm = image.get((x + 1, y))
    right = perms[right_perm[0]][right_perm[1]] if right_perm else None
    return [
        (tile_id, tile_perm_id)
        for tile_id, tile_perms in perms.items()
        if tile_id not in placed
        for tile_perm_id, tile_perm in enumerate(tile_perms)
        if fits(tile_perm, up, left, down, right)
    ]

def fits(tile, up, left, down, right):
    return all((
        not up or tile[0] == up[-1],
        not down or tile[-1] == down[0],
        not left or [r[0] for r in tile] == [r[-1] for r in left],
        not right or [r[-1] for r in tile] == [r[0] for r in right],
    ))

def merge_tiles(image, perms, idim):
    tdim = DIM - 2
    merged = [[] for _ in range(idim * tdim)]
    for ix in range(idim):
        for iy in range(idim):
            i_tile_id, i_perm_id = image[(ix, iy)]
            tile = perms[i_tile_id][i_perm_id]
            for y, row in enumerate(tile[1:-1]):
                merged[iy * tdim + y] += row[1:-1]
    return merged

def find_monsters(image, pattern):
    w, h = len(image[0]), len(image)
    num_monsters = 0
    for x in range(w):
        for y in range(h):
            for px, py in pattern:
                ix, iy = x + px, y + py
                if not 0 <= ix < w or not 0 <= iy < h:
                    break
                if image[iy][ix] != "#":
                    break
            else:
                num_monsters += 1
    return num_monsters

if __name__ == "__main__":
    main()
