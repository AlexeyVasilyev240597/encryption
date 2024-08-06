from enum import IntEnum

from encryptor import Mode
from file_manager import FileManager
from params import *

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit
    
class Stage(IntEnum):
    START = 0,
    MODE  = 1,
    FILES = 2,
    CRYPT = 3,

class MyButton(QPushButton):
    def __init__(self, text, parent, method_to_connect, pos = Pos.CENTER):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet("font-size: 16px;")
        sizes = scale_on_grid([1, 1])
        self.setFixedSize(sizes[0], sizes[1])
        self.clicked.connect(method_to_connect)
        pos = shift_on_grid([ALIGN[pos], 0])
        self.move(pos[0], pos[1])
        self.vis = False
        self.set_vis()
    
    def change_vis(self):
        self.vis = not self.vis
        self.set_vis()
        
    def set_vis(self):
        self.setDisabled(not self.vis)
        self.setVisible(self.vis)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.stage = Stage.START
        self.mode = Mode.EN
        
        self.setWindowTitle("Encryptor")
        ws = scale_on_grid(WINDOW_SIZE)
        self.setFixedSize(QSize(ws[0], ws[1]))
        
        self.reset_btn = MyButton(
            "RESET",
            self,
            self.reset,
            Pos.LEFT
        )
        self.reset_btn.change_vis()
        
        self.next_btn = MyButton(
            "NEXT",
            self,
            self.next_stage,
            Pos.RIGHT
        )
        self.next_btn.change_vis()
        
        
        self.message_box = QPlainTextEdit(parent=self)
        ms = scale_on_grid([6, 5])
        self.message_box.setFixedSize(ms[0], ms[1])
        mp = shift_on_grid([0, 2])
        self.message_box.move(mp[0], mp[1])
        self.message_box.setReadOnly(True)
                
        # MODE stage        
        self.mode_btn = MyButton(
            Mode.EN.name,
            self,
            self.switch_mode
        )        
    
        # CRYPT stage
        self.key_box = QPlainTextEdit(parent=self)
        ks = scale_on_grid([4, 3])
        self.key_box.setFixedSize(ks[0], ks[1])
        kp = shift_on_grid([7, 2])
        self.key_box.move(kp[0] ,kp[1])
        self.key_box.setReadOnly(True)
        
        self.reset()

    def reset(self):
        if self.stage == Stage.MODE:
            self.mode_btn.change_vis()
        self.stage = Stage.START
        self.message_box.setPlainText("")
        self.reset_btn.change_vis()
        self.key_box.setPlainText("")
        
    def switch_mode(self):
        self.mode = Mode(-self.mode.value)
        self.mode_btn.setText(self.mode.name)
        self.show_file_pairs()
    
    def show_file_pairs(self):
        self.message_box.setPlainText(
            '\n'.join(
                [
                    name + ' -> ' + new_name 
                    for name, new_name 
                    in zip(fm.files_names, fm.new_files_names[self.mode])
                ]
                )
            )
    
    def next_stage(self):
        print(f'I am in next stage, cur stage is {self.stage.name}')
        if self.stage == Stage.START:
            if self.pick_working_dir():
                self.mode_btn.change_vis()
                fm.transform_names()
                self.show_file_pairs()
                self.reset_btn.change_vis()
            else:
                print("WD is not set")
                return
        elif self.stage == Stage.MODE:
            self.mode_btn.change_vis()
        elif self.stage == Stage.FILES:
            if self.choose_files():
                self.show_file_pairs()
                self.key_box.setReadOnly(False)
            else:
                print("Files are not chosen")
                return
        elif self.stage == Stage.CRYPT:
            if self.crypt_files():
                print("Done")
                self.reset()
            return
        # self.stage = Stage((self.stage.value + 1) % len(Stage))
        self.stage = Stage(self.stage.value + 1)
    
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
        return fm.transform_content(self.key_box.toPlainText())

app = QApplication([])

fm = FileManager()

window = Window()


window.show()
app.exec()