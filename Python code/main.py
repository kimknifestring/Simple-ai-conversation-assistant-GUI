from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QTextEdit, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView
import sys
import os
import threading
from animation import ResizingBot
from taking import record_audio,transcribe_audio
from conversation import generate_response
import re
import pyttsx3



class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        
        # Title Label
        self.setWindowTitle("임시GUI")
        self.setGeometry(100, 100, 400, 600)
        
        self.layout = QVBoxLayout()
        
        self.title_label = QLabel("Chat App")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            padding: 10px;
            border-radius: 15px;
            border: 1px solid white;
            background: qlineargradient(spread:pad, x1:0, y1:0, x5:4, y5:4, 
                        stop:0 #a1c4fd, 
                        stop:1 #c2e9fb);
        """)
        self.layout.addWidget(self.title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: white; padding: 10px; border: none; border-radius: 15px;")
        self.layout.addWidget(self.text_edit)

        self.input_layout = QVBoxLayout()
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("padding: 10px; border-radius: 15px; border: 2px solid #ccc;")
        self.input_layout.addWidget(self.input_line)
        
        self.send_button = QPushButton("전송")
        self.send_button.setStyleSheet(" border: 2px solid blue; background-color: white; color: black; border-radius: 15px; padding: 10px;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        self.record_button = QPushButton("음성 입력")
        self.record_button.setStyleSheet("border: 2px solid green; background-color: white; color: black; border-radius: 15px; padding: 10px;")
        self.record_button.clicked.connect(self.record_and_transcribe)
        self.input_layout.addWidget(self.record_button)
        
        self.layout.addLayout(self.input_layout)
        
        self.setLayout(self.layout)
        
        self.setLayout(self.layout)

    def send_message(self):
        user_message = self.input_line.text()
        if user_message:
            gen_respon = generate_response(user_message)
            response = f"\"{gen_respon}\"" 
            self.text_edit.append(f"User: {user_message}")
            self.text_edit.append(f"Bot:{response}")
            self.input_line.clear()

    
    def record_and_transcribe(self):
        def record_thread():
            record_audio("recorded.wav")
            transcript = transcribe_audio("recorded.wav")
            self.input_line.setText(transcript)

        thread = threading.Thread(target=record_thread)
        thread.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    


class ImageWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QVBoxLayout()


        self.image_label = ResizingBot(image_path)
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.drag_position = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft();

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.drag_position = None

"""class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft();

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.drag_position = None"""


app = QApplication(sys.argv)

script_dir = os.path.dirname(os.path.abspath(__file__))
img_file = os.path.join(script_dir, '../imgs/test.png')
image_window = ImageWindow(img_file)
image_window.show()

main_window = MainApp()
main_window.show()

sys.exit(app.exec_())
