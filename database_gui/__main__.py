import psycopg2
import sys
from os import getenv

from dotenv import load_dotenv
from PyQt5.QtWidgets import (
	QApplication, QWidget, QTabWidget,
	QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
	QTableWidget, QGroupBox, QTableWidgetItem,
	QPushButton, QMessageBox
)
from .database_table_widget import QDatabaseTableWidget

load_dotenv()


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self._connect_to_db()
		self.setWindowTitle("Schedule")

		self.vbox = QVBoxLayout(self)
		self.vbox.addWidget(QDatabaseTableWidget(self.conn, "bot", "timetable"))
		self.setLayout(self.vbox)

	def _connect_to_db(self):
		self.conn = psycopg2.connect(
			database=getenv("PG_DATABASE"),
			user=getenv("PG_USER"), password=getenv("PG_PASSWORD"),
			host=getenv("PG_HOST"), port=getenv("PG_PORT")
		)
		self.cursor = self.conn.cursor()


def main():
	app = QApplication(sys.argv)

	win = MainWindow()
	win.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
