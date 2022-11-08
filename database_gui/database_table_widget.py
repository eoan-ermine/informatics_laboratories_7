import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, ForeignKeyViolation, InvalidTextRepresentation

from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import (
	QWidget, QTableWidgetItem, QAbstractScrollArea,
	QTableWidget, QPushButton, QHBoxLayout,
	QSizePolicy, QMessageBox
)

from .table_widget_button import QTableWidgetButton


class QDatabaseTableWidget(QTableWidget):
	def __init__(self, connection, schema_name: str, table_name: str, predicate: str = None):
		super().__init__()

		self.connection = connection
		self.cursor = connection.cursor(cursor_factory=RealDictCursor)
		
		self.schema_name, self.table_name, self.predicate = schema_name, table_name, predicate
		self.column_names = []
		self.buttons_offset = None

		self.current_row = 0

		self._initialize_table_widget()
		self.update_contents()

	def _retrieve_rows(self):
		select_query = f"SELECT * FROM {self.schema_name}.{self.table_name}"
		if self.predicate:
			select_query = select_query + f" WHERE {self.predicate}"

		self.cursor.execute(select_query)
		return self.cursor.fetchall()

	def _append_row(self, **data):
		for i, value in enumerate(data.values()):
			self.setItem(self.current_row, i, QTableWidgetItem(str(value)))

		update_button = QTableWidgetButton("Update")
		update_button.clicked.connect(lambda state, row=self.current_row, row_id=data["id"]: self._update_row(row, row_id))
		self.setCellWidget(self.current_row, self.buttons_offset, update_button)

		delete_button = QTableWidgetButton("Delete")
		delete_button.clicked.connect(lambda state, row_id=data["id"]: self._delete_row(row_id))
		self.setCellWidget(self.current_row, self.buttons_offset + 1, delete_button)

		self.current_row += 1

	def _append_mother_row(self):
		current_row = self.rowCount() - 1

		create_button = QTableWidgetButton("Create")
		create_button.clicked.connect(lambda state, row=self.current_row: self._create_row(row))
		self.setCellWidget(current_row, self.buttons_offset, create_button)

	def _initialize_table_widget(self):
		self.clear()
		self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s", (self.schema_name, self.table_name,))
		self.column_names = [dict(row)["column_name"] for row in self.cursor.fetchall()]
		self.buttons_offset = len(self.column_names)

		self.setColumnCount(len(self.column_names) + 2) # Update (create) button, delete button
		self.setHorizontalHeaderLabels(self.column_names + ["", ""])

	def update_contents(self):
		self.clearContents()

		rows = self._retrieve_rows()
		self.setRowCount(len(rows) + 1) # One more row for mother row
		self.current_row = 0

		for i, row in enumerate(rows):
			self._append_row(**row)
		self._append_mother_row()

		self.resizeColumnsToContents()


	def _create_row(self, row_idx: int):
		try:
			column_values = tuple([self.item(row_idx, i).text() for i in range(len(self.column_names))])
		except AttributeError:
			QMessageBox.critical(self, "Операция невозможна", "Пожалуйста, заполните значениями все колонки")
			return

		column_names = ','.join(self.column_names)
		values = ','.join(['%s' for _ in range(len(self.column_names))])

		try:
			self.cursor.execute(f"INSERT INTO {self.schema_name}.{self.table_name}({column_names}) VALUES({values})", column_values)
		except UniqueViolation:
			QMessageBox.critical(self, "Операция невозможна", "Строка с указанным идентификатором уже существует. Пожалуйста, измените идентификатор на уникальный и повторите попытку")
			return

		self.update_contents()

	def _update_row(self, row_idx: int, row_id: int):
		column_values = [self.item(row_idx, i).text() for i in range(len(self.column_names))]

		column_updates = ",".join(f"{column_name}=%s" for column_name in self.column_names)
		
		try:
			self.cursor.execute(f"UPDATE {self.schema_name}.{self.table_name} SET {column_updates} WHERE id = %s", (*tuple(column_values), str(row_id)))
		except InvalidTextRepresentation:
			QMessageBox.critical(self, "Операция невозможна", "Некорректное значение колонки (колонок). Пожалуйста, измените значение (значения) на корректные и повторите попытку")
		except ForeignKeyViolation:
			QMessageBox.critical(self, "Операция невозможна", "Нарушение foreign key ограничения. Пожалуйста, устраните его и повторите попытку")

		self.update_contents()

	def _delete_row(self, row_id: int):
		self.cursor.execute(f"DELETE FROM {self.schema_name}.{self.table_name} WHERE id = %s", (row_id,))
		self.update_contents()
