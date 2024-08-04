from enum import IntEnum


BLOCK_SIZE = 60

scale_on_grid = lambda sizes: [BLOCK_SIZE*sizes[0], BLOCK_SIZE*sizes[1]]
shift_on_grid = lambda pos: [BLOCK_SIZE*pos[0] + BLOCK_SIZE//2, BLOCK_SIZE*pos[1] + BLOCK_SIZE//2]

WINDOW_SIZE = [12, 8]

class Pos(IntEnum):
    LEFT = 0,
    CENTER = 1,
    RIGHT = 2

ALIGN = {
    Pos.LEFT: 0,
    Pos.CENTER: (WINDOW_SIZE[0] - 1) // 2,
    Pos.RIGHT: (WINDOW_SIZE[0] - 2)
    }
