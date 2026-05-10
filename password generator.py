import sys
import random
import string
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QCheckBox, 
                             QFrame, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class PasswordApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 1. Window Configuration
        self.setWindowTitle("Professional Password Generator")
        self.setFixedSize(500, 580) 
        self.setStyleSheet("background-color: #f4f7f9;")

        main_layout = QVBoxLayout()
        
        # Fixed Margins based on user requirement (L: 40, T: 10, R: 20, B: 55)
        main_layout.setContentsMargins(40, 10, 20, 55) 
        main_layout.setSpacing(10)

        # 2. Result Display Section
        result_card = QFrame()
        result_card.setFixedHeight(115)
        result_card.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d1d4d9;")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(15, 10, 15, 10)

        res_row = QHBoxLayout()
        res_row.addWidget(QLabel("Password:"))
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Ready to generate...")
        self.result_display.setStyleSheet("border: 1px solid #ced4da; padding: 8px; font-family: 'Consolas'; background: #f8f9fa;")
        res_row.addWidget(self.result_display)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setFixedWidth(70)
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setStyleSheet("""
            QPushButton { background: #27ae60; color: white; font-weight: bold; height: 32px; border-radius: 5px; border: none; }
            QPushButton:hover { background: #2ecc71; }
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        res_row.addWidget(self.copy_btn)
        result_layout.addLayout(res_row)

        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Strength:"))
        self.status_lbl = QLabel("---")
        self.status_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.status_lbl.setStyleSheet("color: #95a5a6;")
        status_row.addWidget(self.status_lbl)
        status_row.addStretch()
        result_layout.addLayout(status_row)
        main_layout.addWidget(result_card)

        # 3. Configuration Section (With specific padding)
        settings_group = QGroupBox(" Configuration ")
        settings_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; border: 1px solid #0088cc; 
                background: white; border-radius: 8px; padding-top: 30px; 
            } 
            QGroupBox::title { left: 15px; color: #0088cc; }
        """)
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setContentsMargins(30, 20, 30, 25) # Internal padding
        settings_layout.setSpacing(22) # Gap between options

        len_row = QHBoxLayout()
        len_row.addWidget(QLabel("Length:"))
        self.len_input = QLineEdit("16")
        self.len_input.setFixedWidth(50)
        self.len_input.setAlignment(Qt.AlignCenter)
        self.len_input.setStyleSheet("border: 1px solid #ccc; border-radius: 3px;")
        len_row.addWidget(self.len_input)
        len_row.addStretch()
        settings_layout.addLayout(len_row)

        self.options = {
            'lower': QCheckBox("Include Lowercase"),
            'upper': QCheckBox("Include Uppercase"),
            'num': QCheckBox("Include Numbers"),
            'sym': QCheckBox("Include Symbols"),
            'sim': QCheckBox("Exclude Similar (o,0,i,l,1)")
        }

        for key, cb in self.options.items():
            cb.setStyleSheet("font-weight: normal; font-size: 13px;")
            if key != 'sim': cb.setChecked(True)
            settings_layout.addWidget(cb)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 15, 0, 0)
        
        self.gen_btn = QPushButton("Generate Password")
        self.gen_btn.setFixedHeight(45)
        self.gen_btn.setCursor(Qt.PointingHandCursor)
        self.gen_btn.setStyleSheet("""
            QPushButton { background: #008cba; color: white; font-weight: bold; border-radius: 6px; border: none; }
            QPushButton:hover { background: #00a3d9; }
        """)
        self.gen_btn.clicked.connect(self.generate_password)
        
        self.adv_btn = QPushButton("Advanced")
        self.adv_btn.setFixedHeight(45)
        self.adv_btn.setStyleSheet("""
            QPushButton { background: #5d6d7e; color: white; font-weight: bold; border-radius: 6px; border: none; }
            QPushButton:hover { background: #7f8c8d; }
        """)
        
        btn_layout.addWidget(self.gen_btn, 2)
        btn_layout.addWidget(self.adv_btn, 1)
        settings_layout.addLayout(btn_layout)
        main_layout.addWidget(settings_group)

        # 4. Footer Branding
        footer_lbl = QLabel("Developed by EVS Technologies")
        footer_lbl.setAlignment(Qt.AlignCenter)
        footer_lbl.setStyleSheet("color: #7f8c8d; font-size: 10px; font-weight: bold; padding-top: 10px;")
        main_layout.addWidget(footer_lbl)

        self.setLayout(main_layout)

    def generate_password(self):
        pool = ""
        if self.options['lower'].isChecked(): pool += string.ascii_lowercase
        if self.options['upper'].isChecked(): pool += string.ascii_uppercase
        if self.options['num'].isChecked(): pool += string.digits
        if self.options['sym'].isChecked(): pool += string.punctuation
        
        if self.options['sim'].isChecked():
            for char in "ol0I1": pool = pool.replace(char, "")

        if not pool:
            self.status_lbl.setText("Select Options!")
            return

        try:
            length = int(self.len_input.text())
            pwd = "".join(random.SystemRandom().choice(pool) for _ in range(length))
            self.result_display.setText(pwd)
            
            if length < 8: 
                self.status_lbl.setText("Weak")
                self.status_lbl.setStyleSheet("color: #e74c3c;")
            elif length < 14: 
                self.status_lbl.setText("Secure")
                self.status_lbl.setStyleSheet("color: #f39c12;")
            else: 
                self.status_lbl.setText("Very Secure")
                self.status_lbl.setStyleSheet("color: #27ae60;")
        except: 
            self.status_lbl.setText("Error")

    def copy_to_clipboard(self):
        text = self.result_display.text()
        if text:
            QApplication.clipboard().setText(text)
            self.status_lbl.setText("Copied!")
            self.status_lbl.setStyleSheet("color: #3498db;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PasswordApp()
    ex.show()
    sys.exit(app.exec())
