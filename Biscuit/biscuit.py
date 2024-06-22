#
# Written by Sean Lewis (slewis.wiki) - 2024
# Buscuit is a bite-sized web browser using PyQt5 and BeautifulSoup.
#
# Any and all of this code may be used by anyone for any purpose.
# I prefer if you give credit if you believe it is due :)
#
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTextBrowser, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap

import requests
from time import time

from bs4 import BeautifulSoup

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BISCUIT")

        # Set up the window layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create the components: URL bar, Go button, and page display
        self.url_bar = QLineEdit()
        self.layout.addWidget(self.url_bar)

        # Go button and actions
        self.go_button = QPushButton("Go")
        self.layout.addWidget(self.go_button)
        self.go_button.clicked.connect(self.load_page)

        # Init page display and welcome message
        self.page_display = QTextBrowser()
        self.page_display.setReadOnly(True)
        self.page_display.setOpenExternalLinks(False)
        self.page_display.anchorClicked.connect(self.handle_clicked_link)
        self.layout.addWidget(self.page_display)
        self.welcome_page = """<html><head></head><body><p>Welcome to BISCUIT ;)</p></body></html>"""
        self.page_display.setHtml(self.welcome_page)

        # Data info label
        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)

        # Menu bar options
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        save_action = QAction("Save Page As", self)
        save_action.triggered.connect(self.save_page)
        file_menu.addAction(save_action)

        settings_menu = menu_bar.addMenu("Settings")
        theme_action = QAction("Change Theme", self)
        theme_action.triggered.connect(self.change_theme)
        settings_menu.addAction(theme_action)

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
        f"HTML Content Size: {content_length} bytes\n"
        f"Header Size: {headers_size} bytes\n"
        f"Loaded In: {tick-tock:.2f} seconds")

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

    def save_page(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "HTML Files (*.html);;All Files (*)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.page_display.toHtml())
                QMessageBox.information(self, "Success", f"Page saved successfully to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save page: {str(e)}")
    
    def change_theme(self):
        return

app = QApplication([])
window = Browser()
window.show()
app.exec_()