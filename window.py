from enum import IntEnum
import json 

from encryptor import Mode
from file_manager import FileManager
from grid import *

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit

# in pixel units
BLOCK_SIZE = 60
# in block units
WINDOW_SIZE = [12, 8]


class Stage(IntEnum):
    START = 0,
    MODE  = 1,
    FILES = 2,
    CRYPT = 3,
    DONE  = 4

class MyButton(QPushButton):
    def __init__(self, text, parent, method_to_connect, sizes, pos):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet("font-size: 16px;")
        self.setFixedSize(grid.scale_on_grid(sizes))
        self.clicked.connect(method_to_connect)
        self.move(grid.shift_on_grid(pos))
        self.vis = False
        self.set_vis()
    
    def change_vis(self):
        self.vis = not self.vis
        self.set_vis()
        
    def set_vis(self):
        self.setDisabled(not self.vis)
        self.setVisible(self.vis)

class MyTextBox(QPlainTextEdit):
    def __init__(self, parent, sizes, pos):
        super().__init__(parent=parent)
        self.setFixedSize(grid.scale_on_grid(sizes))
        self.move(grid.shift_on_grid(pos))
        self.setFont(QFont("Courier"))
        self.setReadOnly(True)
        
        
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.stage = Stage.START
        
        self.setWindowTitle("Encryptor")
        self.setFixedSize(grid.scale_on_grid(grid.ws))
        
        self.init_widgets("widgets.json")
        # self.widgets["RESET"] = MyButton(
        #     "RESET",
        #     self,
        #     self.reset,
        #     Pos.LEFT
        # )
        self.widgets["RESET"].change_vis()
        
        # self.widgets["NEXT"] = MyButton(
        #     "NEXT",
        #     self,
        #     self.next_stage,
        #     Pos.RIGHT
        # )
        self.widgets["NEXT"].change_vis()
        
        
        # self.widgets["MESSAGE"] = MyTextBox(parent=self)        
                
        # # MODE stage        
        # self.mode_btn = MyButton(
        #     Mode.EN.name,
        #     self,
        #     self.switch_mode
        # )        
    
        # # CRYPT stage
        # self.widgets["KEY"] = MyTextBox(parent=self)
        
        self.reset()

    def init_widgets(self, json_fn):
        json_f = open(json_fn)
        widgets = json.load(json_f)
        
        self.widgets = {}
        for widget in widgets:
            print(f"Widget name: {widget['Name']}")
            pos = grid.convert_pos(widget["Pos"], widget["Sizes"])
            if widget["Type"] == "button":
                self.widgets[widget["Name"]] = MyButton(
                    widget["Name"], 
                    self, 
                    getattr(self, widget["Action"]),
                    widget["Sizes"],
                    pos)
            elif widget["Type"] == "text_box":
                self.widgets[widget["Name"]] = MyTextBox(self, widget["Sizes"], pos)
            else:
                print(f"Undefined widget type: {widget['Type']}")
        
        json_f.close()

    def reset(self):
        if self.stage == Stage.MODE:
            self.widgets["MODE"].change_vis()
        elif self.stage == Stage.DONE:
            self.widgets["NEXT"].change_vis()
        self.stage = Stage.START
        self.mode = Mode.EN
        self.widgets["MODE"].setText(self.mode.name)
        self.widgets["MESSAGE"].setPlainText("")
        self.widgets["RESET"].change_vis()
        self.widgets["KEY"].setPlainText("")
        self.widgets["KEY"].setReadOnly(True)
        self.widgets["NEXT"].setText(self.stage.name)
        
    def switch_mode(self):
        self.mode = Mode(-self.mode.value)
        self.widgets["MODE"].setText(self.mode.name)
        self.show_file_pairs()
    
    def show_file_pairs(self):
        M = max([len(name) for name in fm.files_names])
        
        self.widgets["MESSAGE"].setPlainText(
            '\n'.join(
                [
                    name + ' '*(M-len(name)) + ' -> ' + new_name 
                    for name, new_name 
                    in zip(fm.files_names, fm.new_files_names[self.mode])
                ]
                )
            )
    
    def next_stage(self):
        print(f'I am in next stage, cur stage is {self.stage.name}')
        if self.stage == Stage.START:
            if self.pick_working_dir():
                self.widgets["MODE"].change_vis()
                fm.transform_names()
                self.show_file_pairs()
                self.widgets["RESET"].change_vis()
            else:
                print("WD is not set")
                return
        elif self.stage == Stage.MODE:
            self.widgets["MODE"].change_vis()
        elif self.stage == Stage.FILES:
            if self.choose_files():
                self.show_file_pairs()
                self.widgets["KEY"].setReadOnly(False)
            else:
                print("Files are not chosen")
                return
        elif self.stage == Stage.CRYPT:
            if self.crypt_files():
                self.widgets["MESSAGE"].setPlainText("Done")
                self.widgets["NEXT"].change_vis()
                self.widgets["KEY"].setPlainText("")
                self.widgets["KEY"].setReadOnly(True)
            else:
                return
        self.stage = Stage(self.stage.value + 1)
        self.widgets["NEXT"].setText(self.stage.name)
    
    def pick_working_dir(self) -> bool:
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select working directory'
        )
        if response:
            fm.set_working_dir(response)
            print(response)
            return True
        else:
            return False
    
    def choose_files(self) -> bool:
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption=f'Select files to {self.mode.name}CRYPT',
            directory=str(fm.working_dir)
        )
        if not len(response[0]) == 0:
            fm.set_files_to_crypt(response[0], self.mode)
            print(response[0])
            return True
        else:
            return False
    
    def crypt_files(self) -> bool:
        return fm.transform_content(self.widgets["KEY"].toPlainText())


app = QApplication([])
grid = Grid(BLOCK_SIZE, WINDOW_SIZE)
fm = FileManager()
window = Window()

window.show()
app.exec()