import psycopg2
from psycopg2.extras import RealDictCursor

from PyQt5 import Qt
from PyQt5.QtWidgets import (
	QWidget, QTableWidgetItem, QAbstractScrollArea
	QTableWidget, QPushButton, QHBoxLayout,
)

class QDatabaseTableWidget(QTableWidget):
	def __init__(self, connection, schema_name: str, table_name: str):
		super().__init__()

		self.connection = connection
		self.cursor = connection.cursor(cursor_factory=RealDictCursor)
		
		self.schema_name = schema_name
		self.table_name = table_name
		self.buttons_offset = None

		self._initialize_table_widget()

	def _retrieve_rows(self):
		self.cursor.execute(f"SELECT * FROM {schema_name}.{table_name}")
		return self.cursor.fetchall()

	def _create_button_widget(self, text: str):
		button = QPushButton()
		button.setText(text)

		layout = QHBoxLayout()
		layout.addWidget(button)
		layout.setAlignment(Qt.AlignCenter)
		layout.setContentsMargins(0, 0, 0, 0)

		widget = QWidget()
		widget.setLayout(layout)

		return (widget, button)

	def _append_row(self, **data, is_mother_row = False):
		current_row = self.rowCount()

		if is_mother_row:
			create_button, create_widget = self._create_button_widget("Create")
			self.setCellWidget(current_row, self.buttons_offset + 1, create_widget)
			return

		data = self._retrieve_rows()
		for i, value in enumerate(data.values()):
			self.setItem(current_row, i, QTableWidgetItem(value))

		update_button, update_widget = self._create_button_widget("Update")
		self.setCellWidget(current_row, self.buttons_offset, update_widget)

		delete_button, delete_widget = self._create_button_widget("Delete")
		self.setCellWidget(current_row, self.buttons_offset + 1, delete_widget)

	def _append_mother_row(self):
		self._append_row(is_mother_row=True)

	def _initialize_table_widget(self):
		self.clear()
		self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE schema_name = ? AND table_name = ?", (self.schema_name, self.table_name,))
		column_names = self.cursor.fetchall()
		self.buttons_offset = len(column_names)

		self.setColumnCount(len(column_names) + 2) # Update button, delete (create) button
		self.setHorizontalHeaderLabels(column_names + ["", ""])

	def _update_contents(self):
		self.clearContents()

		rows = self._retrieve_rows()
		self.setRowCount(len(rows) + 1) # One more row for mother row

		for row in rows:
			self._append_row(**row)
		self._append_mother_row()
