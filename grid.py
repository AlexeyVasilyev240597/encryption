from PyQt6.QtCore import QObject, QSize, QPoint

class Grid(QObject):
    def __init__(self, bs: int, ws: list) -> None:
        # block size
        self.bs = bs
        # window sizes in block units
        self.ws = ws
           
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
                pos_n.append((self.ws[i] - 1) // 2)
            elif n == "LEFT":
                pos_n.append(0)
            elif n == "RIGHT":
                pos_n.append(self.ws[0] - sizes[0] - 1)
            elif n == "TOP":
                pos_n.append(0)
            elif n == "BOTTOM":
                pos_n.append(self.ws[1] - sizes[1] - 1)
        return pos_n
    
