from enum import IntEnum

from file_manager import FileManager

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit

WINDOW_HEIGHT = 600
WINDOW_WIDTH  = 800

BUTTON_HEIGHT = 60
BUTTON_WIDTH  = 120

class Stage(IntEnum):
    START = 0,
    MODE  = 1,
    FILES = 2,
    RUN   = 3,
    RESET = 4

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryptor")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self._init_buttons()
        
        self.text_box = QPlainTextEdit(parent=self)
        self.text_box.setFixedSize(4 * BUTTON_WIDTH, 5 * BUTTON_HEIGHT)
        self.text_box.move(WINDOW_WIDTH // 2 - 2 * BUTTON_WIDTH, 2 * BUTTON_HEIGHT)
        self.text_box.setReadOnly(True)
        
        # layout = QVBoxLayout()
        # layout.addWidget(start_button)
        # self.setLayout(layout)

    def _init_buttons(self):
        self.buttons = {}
        stage_to_method = {
            Stage.START: self.pick_working_dir,
            Stage.MODE:  self.set_mode,
            Stage.FILES: self.choose_files,
            Stage.RUN:   self.crypt_files,
            Stage.RESET: self.next_stage
        }
        for stage in Stage:
            self._add_button(stage, stage_to_method[stage])
        # init stage
        self.stage = Stage(0)
        self.buttons[self.stage].setDisabled(False)

    def _add_button(self, stage, method_to_connect):
        button = QPushButton(text=stage.name, parent=self)
        button.setStyleSheet("font-size: 16px;")
        button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        # TODO: create a dict
        button.clicked.connect(method_to_connect)
        button.move((WINDOW_WIDTH * (2 * stage.value + 1) // len(Stage) - BUTTON_WIDTH) // 2, 
                    BUTTON_HEIGHT // 2)
        button.setDisabled(True)
        self.buttons[stage] = button
    
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
        self.next_stage()
        print(response)

    def set_mode(self):
        pass
    
    def choose_files(self):
        pass
    
    def crypt_files(self):
        pass

app = QApplication([])
fm = FileManager()
window = Window()
window.show()
app.exec()