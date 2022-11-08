from PyQt5.QtWidgets import QPushButton, QSizePolicy


class QTableWidgetButton(QPushButton):
    def __init__(self, text: str):
        super().__init__()

        self.setText(text)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
