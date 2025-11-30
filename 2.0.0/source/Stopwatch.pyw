import sys
import os
import time
from datetime import timedelta
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class Stopwatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stopwatch")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 440, 140)
        self.setMinimumSize(440, 140)
        self.setStyleSheet("""
            QMainWindow {background-color:#2e2e2e;}
            QLabel {color:white;font-family:Courier;font-size:24px;}
            QPushButton {background-color:#000000;color:white;border-radius:5px;}
            QPushButton:hover {background-color:#232323;}
            QPushButton:pressed {background-color:#333333;}
            QPushButton:disabled {background-color:#464646;color:white;}
        """)
        central = QWidget()
        self.setCentralWidget(central)
        v_layout = QVBoxLayout(central)
        self.time_label = QLabel("0:00:00.000000")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(self.time_label)
        btn_layout = QHBoxLayout()
        v_layout.addLayout(btn_layout)
        button_height = 30
        scaled_height = int(button_height * 1.6)
        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedHeight(scaled_height)
        self.start_btn.clicked.connect(self.start)
        btn_layout.addWidget(self.start_btn)
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setFixedHeight(scaled_height)
        self.pause_btn.clicked.connect(self.pause_resume)
        self.pause_btn.setEnabled(False)
        btn_layout.addWidget(self.pause_btn)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedHeight(scaled_height)
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        self.restart_btn = QPushButton("Restart")
        self.restart_btn.setFixedHeight(scaled_height)
        self.restart_btn.clicked.connect(self.restart)
        self.restart_btn.setEnabled(False)
        btn_layout.addWidget(self.restart_btn)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedHeight(scaled_height)
        self.reset_btn.clicked.connect(self.reset)
        btn_layout.addWidget(self.reset_btn)
        self.running = False
        self.paused = False
        self.start_time = None
        self.elapsed = timedelta(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1)
        self.update_buttons()

    def update_time(self):
        if self.running:
            now = time.time()
            diff = timedelta(seconds=now - self.start_time) + self.elapsed
        else:
            diff = self.elapsed
        total_seconds = diff.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        microseconds = diff.microseconds
        self.time_label.setText(f"{hours}:{minutes:02d}:{seconds:02d}.{microseconds:06d}")
        self.update_buttons()

    def update_buttons(self):
        self.start_btn.setEnabled(not self.running and not self.paused)
        self.pause_btn.setEnabled(self.running or self.paused)
        self.pause_btn.setText("Resume" if self.paused else "Pause")
        self.stop_btn.setEnabled(self.running)
        self.restart_btn.setEnabled(self.running or self.paused)
        zero_time = self.elapsed.total_seconds() == 0 and not self.running and not self.paused
        self.reset_btn.setEnabled(not zero_time)

    def start(self):
        self.start_time = time.time()
        self.running = True
        self.paused = False
        self.update_buttons()

    def pause_resume(self):
        if self.running:
            now = time.time()
            self.elapsed += timedelta(seconds=now - self.start_time)
            self.running = False
            self.paused = True
        elif self.paused:
            self.start_time = time.time()
            self.running = True
            self.paused = False
        self.update_buttons()

    def stop(self):
        if self.running:
            now = time.time()
            self.elapsed += timedelta(seconds=now - self.start_time)
        self.running = False
        self.paused = False
        self.update_buttons()

    def restart(self):
        self.elapsed = timedelta(0)
        self.start_time = time.time()
        self.running = True
        self.paused = False
        self.update_buttons()

    def reset(self):
        if self.running:
            now = time.time()
            self.elapsed += timedelta(seconds=now - self.start_time)
        self.elapsed = timedelta(0)
        self.start_time = None
        self.running = False
        self.paused = False
        self.update_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Stopwatch()
    window.show()
    sys.exit(app.exec())
