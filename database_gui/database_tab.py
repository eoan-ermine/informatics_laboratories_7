from PyQt5.QtWidgets import (
	QWidget, QVBoxLayout, QLabel,
	QPushButton
)

class QDatabaseTabItem(QWidget):
	def __init__(self, widget, caption = None):
		super().__init__()

		self.widget, self.caption = widget, caption

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		if caption:
			self.layout.addWidget(QLabel(caption))
		self.layout.addWidget(widget)

	def getWidget(self):
		return self.widget


class QDatabaseTab(QWidget):
	def __init__(self, items: list[QDatabaseTabItem] = []):
		super().__init__()

		self.items = items
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		update_button = QPushButton("Update")
		update_button.clicked.connect(lambda state, _=None: self.update_contents())
		self.layout.addWidget(update_button)
		
		for item in items:
			self.layout.addWidget(item)

	def update_contents(self):
		for item in self.items:
			item.getWidget().update_contents()

	def addItem(self, item: QDatabaseTabItem):
		self.items.append(item)
		self.layout.addWidget(item)
