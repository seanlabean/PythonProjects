#
# Written by Sean Lewis (slewis.wiki) - 2024
# Buscuit is a bite-sized web browser using PyQt5 and BeautifulSoup.
#
# Any and all of this code may be used by anyone for any purpose.
# I prefer if you give credit if you believe it is due :)
#
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTextBrowser

import requests
from time import time

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

        self.page_display = QTextBrowser()
        self.page_display.setReadOnly(True)
        self.page_display.setOpenExternalLinks(False)
        self.page_display.anchorClicked.connect(self.handle_clicked_link)
        self.layout.addWidget(self.page_display)

        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

    def load_page(self):
        """
        Load the web page content from the URL using the BeautifulSoup html parser.
        """
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        tock = time()
        response = requests.get(url)
        content_length = len(response.content)
        headers_size = sum(len(key) + len(value) for key, value in response.headers.items())
        total_size = content_length + headers_size

        soup = BeautifulSoup(response.content, 'html.parser')
        self.page_display.setHtml(soup.prettify())
        parsed_length = len(soup.prettify())
        tick = time()

        self.info_label.setText(f"Total Data Received: {total_size} bytes\n"
        f"HTML Content Size: {content_length}\n"
        f"Headers Size: {headers_size} bytes\n"
        f"Time To Load: {tick-tock:.2f} seconds")

        self.url_bar.setText(url)

    def handle_clicked_link(self, url):
        current_url_text = self.url_bar.text()
        inc_url_text = url.toString()
        if "https" in inc_url_text or "http" in inc_url_text:
            url_str =inc_url_text
        else:
            url_str = ""
            for ext in current_url_text.split('/')[2:]:
                if ext != current_url_text.split('/')[-1] or len(current_url_text.split('/')) == 3:
                    url_str += ext+"/"
            url_str += inc_url_text
        self.url_bar.setText(url_str)
        self.load_page()

app = QApplication([])
window = Browser()
window.show()
app.exec_()
