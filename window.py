from enum import IntEnum

from encryptor import Mode
from file_manager import FileManager

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QPlainTextEdit

BLOCK_SIZE = 60

WINDOW_HEIGHT = 8*BLOCK_SIZE
WINDOW_WIDTH  = 12*BLOCK_SIZE

scale_on_grid = lambda sizes: [BLOCK_SIZE*sizes[0], BLOCK_SIZE*sizes[1]]
shift_on_grid = lambda pos: [BLOCK_SIZE*pos[0] + BLOCK_SIZE//2, BLOCK_SIZE*pos[1] + BLOCK_SIZE//2]
    
class Stage(IntEnum):
    START = 0,
    MODE  = 1,
    FILES = 2,
    CRYPT   = 3,

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.stage = Stage.START
        self.mode = Mode.EN
        
        self.setWindowTitle("Encryptor")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # self._init_stage_buttons()
        self.reset_btn = self._add_button(
            "RESET",
            self.reset,
            [1, 1],
            [0, 0],
            False,
            True
        )
        
        self.reset_btn = self._add_button(
            "NEXT",
            self.next_stage,
            [1, 1],
            [10, 0],
            False,
            True
        )
        
        
        self.message_box = QPlainTextEdit(parent=self)
        ms = scale_on_grid([6, 5])
        self.message_box.setFixedSize(ms[0], ms[1])
        mp = shift_on_grid([0, 2])
        self.message_box.move(mp[0], mp[1])
        self.message_box.setReadOnly(True)
        
        # START stage        
        self.start_btn = self._add_button(
            Stage.START.name,
            self.pick_working_dir,
            [1, 1],
            [5, 0],
            False,
            True
        )
        
        # MODE stage        
        self.mode_btn = self._add_button(
            Mode.EN.name,
            self.switch_mode,
            [1, 1],
            [5, 0],
        )
        
    
        # CRYPT stage
        self.key_box = QPlainTextEdit(parent=self)
        ks = scale_on_grid([4, 3])
        self.key_box.setFixedSize(ks[0], ks[1])
        kp = shift_on_grid([7, 2])
        self.key_box.move(kp[0] ,kp[1])
        self.message_box.setReadOnly(True)
        
        # layout = QVBoxLayout()
        # layout.addWidget(start_button)
        # self.setLayout(layout)
        self.reset()


    def _add_button(self, text, method_to_connect, sizes, pos, disabled = True, vis = False):
        button = QPushButton(text=text, parent=self)
        button.setStyleSheet("font-size: 16px;")
        sizes = scale_on_grid(sizes)
        button.setFixedSize(sizes[0], sizes[1])
        button.clicked.connect(method_to_connect)
        pos = shift_on_grid(pos)
        button.move(pos[0], pos[1])
        button.setDisabled(disabled)
        button.setVisible(vis)
        return button

    def reset(self):
        self.stage = Stage.START
        self.message_box.setPlainText("")
        self.mode_btn.setDisabled(True)
        self.mode_btn.setVisible(False)
        
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
            self.start_btn.setDisabled(True)
            self.start_btn.setVisible(False)
            self.mode_btn.setDisabled(False)
            self.mode_btn.setVisible(True)
            fm.transform_names()
            self.show_file_pairs()
        elif self.stage == Stage.MODE: 
            self.mode_btn.setDisabled(True)
            self.mode_btn.setVisible(False)
        elif self.stage == Stage.FILES:
            self.choose_files()
            self.show_file_pairs()
        elif self.stage == Stage.CRYPT:
            self.message_box.setReadOnly(False)
            self.crypt_files()
        self.stage = Stage((self.stage.value + 1) % len(Stage))
    
    # source: https://learndataanalysis.org/source-code-how-to-use-qfiledialog-file-dialog-in-pyqt5/
    def pick_working_dir(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select working directory'
        )
        fm.set_working_dir(response)
        files_list = '\n'.join(fm.files_names)
        self.message_box.setPlainText(files_list)
        print(response)
    
    def choose_files(self):
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption=f'Select files to {self.mode.name}CRYPT',
            directory=str(fm.working_dir)
        )
        fm.set_files_to_crypt(response[0], self.mode)
    
    def crypt_files(self):
        fm.transform_content(self.key_box.toPlainText())

app = QApplication([])

fm = FileManager()

window = Window()


window.show()
app.exec()