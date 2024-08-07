from PyQt6.QtCore import QSize, QPoint

from enum import IntEnum

WINDOW_SIZE = [12, 8]

# class Axis(IntEnum):
#     X = 0,
#     Y = 1

class Pos(IntEnum):
    LEFT   = 0,
    CENTER = 1,
    RIGHT  = 2,
    BOTTOM = 3,
    TOP    = 4

 
ALIGN = {
    Pos.LEFT:   0,
    Pos.CENTER: (WINDOW_SIZE[0] - 1) // 2,
    Pos.RIGHT:  (WINDOW_SIZE[0] - 2)
}

#   0 1 2 3 4 5 6 7 8 9 10
# 0 * o o * * o * * o o *
# 1 * * * * * * * * * * *
# 2 / - - - - \ * / - - \
# 3 |         | * |     |
# 4 |         | * \ - - /
# 5 |         | * * * * *
# 6 \ - - - - / * * * * *


class Grid:
    def __init__(self, bs: int, ws: list) -> None:
        # block size
        self.bs = bs
        # window sizes in block units
        self.ws = ws
    
    # def align(self, ):
    #     if pos == Pos.LEFT or pos == Pos.TOP:
           
    def scale_on_grid(self, sizes: int) -> list: 
        return QSize(self.bs*sizes[0], self.bs*sizes[1])
    
    def shift_on_grid(self, pos: int) -> list:
        return QPoint(self.bs*pos[0] + self.bs//2, self.bs*pos[1] + self.bs//2)
    
    def convert_pos(self, pos, sizes):
        pos_n = []
        for i in range(len(pos)):
            n = pos[i]
            if str(n).isdigit():
                pos_n.append(n)
            elif n == "CENTER":
                pos_n.append((WINDOW_SIZE[i] - 1) // 2)
            elif n == "LEFT":
                pos_n.append(0)
            elif n == "RIGHT":
                pos_n.append(WINDOW_SIZE[0] - sizes[0] - 1)
            elif n == "TOP":
                pos_n.append(0)
            elif n == "BOTTOM":
                pos_n.append(WINDOW_SIZE[1] - sizes[1] - 1)
        return pos_n
    
