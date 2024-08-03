from enum import IntEnum

from encryptor import Mode
from file_manager import FileManager

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit

WINDOW_HEIGHT = 600
WINDOW_WIDTH  = 800

BUTTON_HEIGHT = 60
BUTTON_WIDTH  = 120

class Stage(IntEnum):
    START = 0,
    CRYPT  = 1,
    FILES = 2,
    RUN   = 3,

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.stage = Stage.START
        self.mode = Mode.EN
        
        self.setWindowTitle("Encryptor")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self._init_stage_buttons()
        self.reset_btn = self._add_button(
            "RESET",
            self.reset,
            [BUTTON_HEIGHT, BUTTON_HEIGHT],
            [WINDOW_WIDTH - BUTTON_HEIGHT, WINDOW_HEIGHT - BUTTON_HEIGHT],
            False
        )
        self.mode_btn = self._add_button(
            self.mode.name,
            self.switch_mode,
            [BUTTON_HEIGHT, BUTTON_HEIGHT],
            [(WINDOW_WIDTH * (2 * Stage.CRYPT.value + 1) // len(Stage) - BUTTON_WIDTH) // 2, BUTTON_HEIGHT // 2],
            False
            )
        
        self.text_box = QPlainTextEdit(parent=self)
        self.text_box.setFixedSize(4 * BUTTON_WIDTH, 5 * BUTTON_HEIGHT)
        self.text_box.move(WINDOW_WIDTH // 2 - 2 * BUTTON_WIDTH, 2 * BUTTON_HEIGHT)
        self.text_box.setReadOnly(True)
        
        # layout = QVBoxLayout()
        # layout.addWidget(start_button)
        # self.setLayout(layout)
        self.reset()

    def _init_stage_buttons(self):
        self.buttons = {}
        stage_to_method = {
            Stage.START: self.pick_working_dir,
            Stage.CRYPT:  self.set_mode,
            Stage.FILES: self.choose_files,
            Stage.RUN:   self.crypt_files
        }
        for stage in Stage:
            w = BUTTON_WIDTH
            h = BUTTON_HEIGHT
            x = (WINDOW_WIDTH * (2 * stage.value + 1) // len(Stage) - BUTTON_WIDTH) // 2
            y = BUTTON_HEIGHT // 2
            if stage == Stage.CRYPT:
                w = w // 2
                x = x + w
            self.buttons[stage] = self._add_button(
                stage.name, 
                stage_to_method[stage], 
                [w, h],
                [x, y],
                True
            )
            self.buttons[stage].clicked.connect(self.next_stage)

    def _add_button(self, text, method_to_connect, sizes, pos, disable):
        button = QPushButton(text=text, parent=self)
        button.setStyleSheet("font-size: 16px;")
        button.setFixedSize(sizes[0], sizes[1])
        button.clicked.connect(method_to_connect)
        button.move(pos[0], pos[1])
        button.setDisabled(disable)
        return button
    
    def reset(self):
        self.buttons[self.stage].setDisabled(True)
        self.stage = Stage.START
        self.buttons[self.stage].setDisabled(False)
        self.text_box.setPlainText("")
        
    def switch_mode(self):
        self.mode = Mode(-self.mode.value)
        self.mode_btn.setText(self.mode.name)
    
    def next_stage(self):
        self.buttons[self.stage].setDisabled(True)
        self.stage = Stage((self.stage.value + 1) % len(Stage))
        self.buttons[self.stage].setDisabled(False)
    
    # source: https://learndataanalysis.org/source-code-how-to-use-qfiledialog-file-dialog-in-pyqt5/
    def pick_working_dir(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select working directory'
        )
        fm.set_working_dir(response)
        files_list = '\n'.join(fm.files_names)
        self.text_box.setPlainText(files_list)
        print(response)

    def set_mode(self):
        fm.transform_names(self.mode)
        self.text_box.setPlainText(
            '\n'.join(
                [
                    name + ' -> ' + new_name 
                    for name, new_name 
                    in zip(fm.files_names, fm.new_files_names)
                ]
                )
            )
        
    
    def choose_files(self):
        pass
    
    def crypt_files(self):
        pass

app = QApplication([])

fm = FileManager()

window = Window()


window.show()
app.exec()