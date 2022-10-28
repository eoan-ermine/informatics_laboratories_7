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


load_dotenv()


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self._connect_to_db()
		self.setWindowTitle("Schedule")

		self.vbox = QVBoxLayout(self)
		self.tabs = QTabWidget(self)
		self.vbox.addWidget(self.tabs)

		self._create_schedule_tab()

	def _connect_to_db(self):
		self.conn = psycopg2.connect(
			database=getenv("PG_DATABASE"),
			user=getenv("PG_USER"), password=getenv("PG_PASSWORD"),
			host=getenv("PG_HOST"), port=getenv("PG_PORT")
		)
		self.cursor = self.conn.cursor()

	def _create_schedule_tab(self):
		self.schedule_tab = QWidget()
		self.tabs.addTab(self.schedule_tab, "Schedule")

		self.monday_gbox = QGroupBox("Monday")

		self.svbox = QVBoxLayout()
		self.shbox1 = QHBoxLayout()
		self.shbox2 = QHBoxLayout()

		self.svbox.addLayout(self.shbox1)
		self.svbox.addLayout(self.shbox2)

		self.shbox1.addWidget(self.monday_gbox)

		self._create_monday_table()

		self.update_schedule_button = QPushButton("Update")
		self.shbox2.addWidget(self.update_schedule_button)
		self.update_schedule_button.clicked.connect(self._update_schedule)

		self.schedule_tab.setLayout(self.svbox)

	def _create_monday_table(self):
		self.monday_table = QTableWidget()
		self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		self.monday_table.setColumnCount(4)
		self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", ", "])

		self._update_monday_table()

		self.mvbox = QVBoxLayout()
		self.mvbox.addWidget(self.monday_table)
		self.monday_gbox.setLayout(self.mvbox)

	def _update_monday_table(self):
		self.cursor.execute("SELECT * FROM bot.timetable WHERE day = 3")
		records = list(self.cursor.fetchall())

		self.monday_table.setRowCount(len(records) + 1)

		for i, r in enumerate(records):
			r = list(r)
			joinButton = QPushButton("join")

			for j in range(3):
				self.monday_table.setItem(i, j, QTableWidgetItem(str(r[j * 2])))
			self.monday_table.setCellWidget(i, 3, joinButton)

			joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

			self.monday_table.resizeRowsToContents()

	def _change_day_from_table(self, rowNum, day):
		row = list()
	
		for i in range(self.monday_table.columnCount()):
			try:
				row.append(self.monday_table.item(rowNum, i).text())
			except:
				row.append(None)

		try:
			self.cursor.execute("TYPE VALID QUERY HERE", tuple(row))
			self.conn.commit()
		except:
			QMessageBox.about(self, "Error", "Enter all fields")

	def _update_schedule(self):
		self._update_monday_table()


def main():
	app = QApplication(sys.argv)

	win = MainWindow()
	win.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
