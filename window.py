
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget

WINDOW_HEIGHT = 800
WINDOW_WIDTH  = 600
BUTTON_HEIGHT = 200
BUTTON_WIDTH  = 80

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryptor")
        self.setFixedSize(QSize(WINDOW_HEIGHT, WINDOW_WIDTH))
        
        start_button = QPushButton(text="Setup Working Directory", parent=self)
        start_button.setStyleSheet("font-size: 16px;")
        start_button.setFixedSize(BUTTON_HEIGHT, BUTTON_WIDTH)
        start_button.clicked.connect(self.pick_working_dir)
        start_button.move((WINDOW_HEIGHT - BUTTON_HEIGHT) // 2, BUTTON_WIDTH // 2)
        
        # layout = QVBoxLayout()
        # layout.addWidget(start_button)        
        
        # self.setLayout(layout)

    
    # source: https://learndataanalysis.org/source-code-how-to-use-qfiledialog-file-dialog-in-pyqt5/
    def pick_working_dir(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select working directory'
        )
        # TODO: pass it to FileManager constructor
        print(response)
        # return response 




app = QApplication([])
window = Window()
window.show()
app.exec()