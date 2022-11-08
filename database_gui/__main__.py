import sys
from os import getenv

import psycopg2
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget

from .database_tab import QDatabaseTab, QDatabaseTabItem
from .database_table_widget import QDatabaseTableWidget

load_dotenv()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._connect_to_db()
        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        self.tabs.addTab(
            QDatabaseTab([QDatabaseTabItem(QDatabaseTableWidget(self.conn, "bot", "subject"))]), "Subjects"
        )

        self.tabs.addTab(
            QDatabaseTab([QDatabaseTabItem(QDatabaseTableWidget(self.conn, "bot", "teacher"))]), "Teachers"
        )

        self.tabs.addTab(
            QDatabaseTab(
                [
                    QDatabaseTabItem(
                        QDatabaseTableWidget(self.conn, "bot", "timetable", f"day={i} ORDER BY week, id"), f"Day #{i}"
                    )
                    for i in range(1, 6)
                ]
            ),
            "Timetable",
        )

        self.vbox.addWidget(self.tabs)
        self.setLayout(self.vbox)

    def _connect_to_db(self):
        self.conn = psycopg2.connect(
            database=getenv("PG_DATABASE"),
            user=getenv("PG_USER"),
            password=getenv("PG_PASSWORD"),
            host=getenv("PG_HOST"),
            port=getenv("PG_PORT"),
        )
        self.conn.set_session(autocommit=True)
        self.cursor = self.conn.cursor()


def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
