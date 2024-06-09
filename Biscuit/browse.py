#
# Written by Sean Lewis (slewis.wiki) - 2024
# Buscuit is a bite-sized web browser using PyQt5 and BeautifulSoup.
#
# Any and all of this code may be used by anyone for any purpose.
# I prefer if you give credit if you believe it is due :)
#
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit
import requests

from bs4 import BeautifulSoup

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biscuit")

        # Set up the window layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create the components: URL bar, Go button, and page display
        self.url_bar = QLineEdit()
        self.layout.addWidget(self.url_bar)

        self.go_button = QPushButton("Go")
        self.layout.addWidget(self.go_button)
        self.go_button.clicked.connect(self.load_page)

        self.page_display = QTextEdit()
        self.layout.addWidget(self.page_display)

    def load_page(self):
        """
        Load the web page content from the URL using the BeautifulSoup html parser.
        """
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.page_display.setHtml(soup.prettify())

app = QApplication([])
window = Browser()
window.show()
app.exec_()
