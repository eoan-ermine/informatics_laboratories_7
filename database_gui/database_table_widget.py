import psycopg2
from psycopg2.extras import RealDictCursor

from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import (
	QWidget, QTableWidgetItem, QAbstractScrollArea,
	QTableWidget, QPushButton, QHBoxLayout,
	QSizePolicy
)

from .table_widget_button import QTableWidgetButton


class QDatabaseTableWidget(QTableWidget):
	def __init__(self, connection, schema_name: str, table_name: str):
		super().__init__()

		self.connection = connection
		self.cursor = connection.cursor(cursor_factory=RealDictCursor)
		
		self.schema_name = schema_name
		self.table_name = table_name
		self.column_names = []
		self.buttons_offset = None

		self._initialize_table_widget()
		self._update_contents()

	def _retrieve_rows(self):
		self.cursor.execute(f"SELECT * FROM {self.schema_name}.{self.table_name}")
		return self.cursor.fetchall()

	def _append_row(self, **data):
		current_row =  data["id"] - 1

		for i, value in enumerate(data.values()):
			self.setItem(current_row, i, QTableWidgetItem(str(value)))

		update_button = QTableWidgetButton("Update")
		update_button.clicked.connect(lambda state, row=current_row, row_id=data["id"]: self._update_row(row, row_id))
		self.setCellWidget(current_row, self.buttons_offset, update_button)

		delete_button = QTableWidgetButton("Delete")
		delete_button.clicked.connect(lambda state, row_id=data["id"]: self._delete_row(row_id))
		self.setCellWidget(current_row, self.buttons_offset + 1, delete_button)

	def _append_mother_row(self):
		current_row = self.rowCount() - 1

		create_button = QTableWidgetButton("Create")
		create_button.clicked.connect(lambda state, row=current_row: self._create_row(row))
		self.setCellWidget(current_row, self.buttons_offset, create_button)

	def _initialize_table_widget(self):
		self.clear()
		self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s", (self.schema_name, self.table_name,))
		self.column_names = [dict(row)["column_name"] for row in self.cursor.fetchall()]
		self.buttons_offset = len(self.column_names)

		self.setColumnCount(len(self.column_names) + 2) # Update (create) button, delete button
		self.setHorizontalHeaderLabels(self.column_names + ["", ""])

	def _update_contents(self):
		self.clearContents()

		rows = self._retrieve_rows()
		self.setRowCount(len(rows) + 1) # One more row for mother row

		for i, row in enumerate(rows):
			self._append_row(**row)
		self._append_mother_row()


	def _create_row(self, row_idx: int):
		column_values = tuple([self.item(row_idx, i).text() for i in range(len(self.column_names))])

		column_names = ','.join(self.column_names)
		values = ','.join(['%s' for _ in range(len(self.column_names))])

		self.cursor.execute(f"INSERT INTO {self.schema_name}.{self.table_name}({column_names}) VALUES({values})", column_values)
		self.connection.commit()
		self._update_contents()

	def _update_row(self, row_idx: int, row_id: int):
		column_values = tuple([self.item(row_idx, i).text() for i in range(len(self.column_names))])
		column_updates = ",".join(f"{column_name}={column_value}" for column_name, column_value in zip(self.column_names, column_values))
		
		self.cursor.execute(f"UPDATE {self.schema_name}.{self.table_name} SET {column_updates} WHERE id = %s", (row_id,))
		self.connection.commit()
		self._update_contents()

	def _delete_row(self, row_id: int):
		self.cursor.execute(f"DELETE FROM {self.schema_name}.{self.table_name} WHERE id = %s", (row_id,))
		self.connection.commit()
		self._update_contents()
