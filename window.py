from enum import IntEnum
import json 

from encryptor import Mode
from file_manager import FileManager
from grid import Grid

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit

class Stage(IntEnum):
    START = 0,
    MODE  = 1,
    FILES = 2,
    CRYPT = 3,
    DONE  = 4

class MyButton(QPushButton):
    def __init__(self, parent, confs):
        pos = parent.convert_pos(confs["Pos"], confs["Sizes"])
        super().__init__(text=confs["Name"], parent=parent)
        self.setStyleSheet("font-size: 16px;")
        self.setFixedSize(parent.scale_on_grid(confs["Sizes"]))
        self.clicked.connect(getattr(parent, confs["Action"]))
        self.move(parent.shift_on_grid(pos))
        self._set_stages(confs["Seeing"])
        self.set_vis(Stage.START)        
    
    def _set_stages(self, seeing):
        is_all = seeing["Stage"] == "all"
        self.stages = [stage 
                       for stage in Stage 
                       if is_all ^ (stage.name == seeing["Except"])]
    
    def set_vis(self, stage):
        vis = stage in self.stages
        self.setDisabled(not vis)
        self.setVisible(vis)


class MyTextBox(QPlainTextEdit):
    def __init__(self, parent, sizes, pos):
        super().__init__(parent=parent)
        self.setFixedSize(parent.scale_on_grid(sizes))
        self.move(parent.shift_on_grid(pos))
        self.setFont(QFont("Courier"))
        self.setReadOnly(True)
        
        
class Window(QWidget, Grid):
    def __init__(self, config_fn):
        QWidget.__init__(self)
        config_f = open(config_fn)
        config = json.load(config_f)
        config_f.close()
        Grid.__init__(self, config["Window"]["Block_size"], config["Window"]["Window_sizes"])
        self.stage = Stage.START
        self.mode = Mode.EN
        
        self.setWindowTitle("Encryptor")
        self.setFixedSize(self.scale_on_grid(self.ws))
        
        self.init_widgets(config["Widgets"])
        
        self.reset()

    def init_widgets(self, widgets):
        self.widgets = {"button": {}, "text_box": {}}
        for widget in widgets:
            # print(f"Widget name: {widget['Name']}")
            pos = self.convert_pos(widget["Pos"], widget["Sizes"])
            if widget["Type"] == "button":
                self.widgets[widget["Type"]][widget["Name"]] = MyButton(self, widget)
            elif widget["Type"] == "text_box":
                self.widgets[widget["Type"]][widget["Name"]] = MyTextBox(self, widget["Sizes"], pos)
            else:
                print(f"Undefined widget type: {widget['Type']}")

    
    def update_buttons(self):
        [button.set_vis(self.stage) for button in self.widgets["button"].values()]

    def reset(self):
        self.stage = Stage.DONE
        self.mode = Mode.EN
        self.widgets["button"]["MODE"].setText(self.mode.name)
        self.next_stage()
        
    def switch_mode(self):
        self.mode = Mode(-self.mode.value)
        self.widgets["button"]["MODE"].setText(self.mode.name)
        self.show_file_pairs()
    
    def show_file_pairs(self):
        M = max([len(name) for name in fm.files_names])
        
        self.widgets["text_box"]["MESSAGE"].setPlainText(
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
                fm.transform_names()
                self.show_file_pairs()
            else:
                print("WD is not set")
                return
        elif self.stage == Stage.FILES:
            if self.choose_files():
                self.show_file_pairs()
                self.widgets["text_box"]["KEY"].setReadOnly(False)
            else:
                print("Files are not chosen")
                return
        elif self.stage == Stage.CRYPT:
            if self.crypt_files():
                self.widgets["text_box"]["MESSAGE"].setPlainText("Done")
                self.widgets["text_box"]["KEY"].setPlainText("")
                self.widgets["text_box"]["KEY"].setReadOnly(True)
        elif self.stage == Stage.DONE:
            self.widgets["text_box"]["MESSAGE"].setPlainText("")
        self.stage = Stage((self.stage.value + 1) % len(Stage))
        self.widgets["button"]["NEXT"].setText(self.stage.name)
        self.update_buttons()
    
    def pick_working_dir(self) -> bool:
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select working directory')
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
        return fm.transform_content(self.widgets["text_box"]["KEY"].toPlainText())


app = QApplication([])
fm = FileManager()
window = Window("config.json")

window.show()
app.exec()