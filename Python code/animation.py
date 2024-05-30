from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import asyncio
from PyQt5.QtCore import QPropertyAnimation, QRect

class ResizingBot(QLabel):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.original_pixmap = QPixmap(image_path)
        self.setPixmap(self.original_pixmap)

        # 이미지 크기 조정 애니메이션
        new_width = int(self.original_pixmap.width() * 3.5)
        new_height = int(self.original_pixmap.height() * 3.5)

        # QLabel의 크기 조정
        self.setFixedSize(new_width, new_height)

        # 이미지 크기 조정
        self.setAlignment(Qt.AlignCenter)  # 이미지를 QLabel 가운데에 정렬
        self.setScaledContents(True)

