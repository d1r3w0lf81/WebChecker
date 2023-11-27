"""
****************************************
*          WebChecker by K3nn3dy         *
****************************************
"""
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import qdarkstyle
from datetime import datetime
import pyttsx3

# Define a class for the Web Scoping application
class WebScopingApp(QWidget):
    def __init__(self):
        super().__init__()

        # List to store URLs
        self.urls = []

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Web Checking Tool')
        self.setGeometry(100, 100, 500, 350)

        # Define fonts
        font_heading = QFont('Helvetica', 16)
        font_label = QFont('Helvetica', 12)

        # Heading label
        self.label_heading = QLabel('Web Checking Tool')
        self.label_heading.setFont(font_heading)
        self.label_heading.setAlignment(Qt.AlignCenter)

        # Description label
        self.label_description = QLabel('Enter a URL or select a file containing URLs. Optionally, enable the WAF check.')
        self.label_description.setFont(font_label)
        self.label_description.setWordWrap(True)

        # URL-related components
        self.label_url = QLabel('Enter URL or Select File:')
        self.label_url.setFont(font_label)

        self.entry_url = QLineEdit(self)
        self.entry_url.setFont(font_label)

        self.button_browse = QPushButton('Browse', self)
        self.button_browse.setFont(font_label)
        self.button_browse.clicked.connect(self.browse_file)

        # WAF check toggle
        self.waf_check_toggle = QCheckBox('Include WAF Check', self)
        self.waf_check_toggle.setFont(font_label)

        # Run button
        self.button_run_scoping = QPushButton('Run Web Check', self)
        self.button_run_scoping.setFont(font_label)
        self.button_run_scoping.clicked.connect(self.run_web_scoping)

        # Layout with increased margins
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_heading)
        layout.addWidget(self.label_description)
        layout.addSpacing(20)  # Increase spacing
        layout.addWidget(self.label_url)
        layout.addWidget(self.entry_url)
        layout.addWidget(self.button_browse)
        layout.addWidget(self.waf_check_toggle)
        layout.addWidget(self.button_run_scoping)
        layout.addSpacing(20)  # Increase spacing

        # Apply QDarkStyle
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def browse_file(self):
        # Function to open file dialog and set the selected file path to the entry field
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select File', '/', 'Text files (*.txt);;All files (*)')
        self.entry_url.setText(file_path)

    def take_screenshot(self, url, output_directory, chromedriver_path):
        # Function to take a screenshot of a website
        options = Options()
        options.add_argument("--headless")

        driver_service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=driver_service, options=options)
        try:
            driver.get(url)
            screenshot_path = os.path.join(output_directory, f"{self.url_to_filename(url)}.png")
            driver.save_screenshot(screenshot_path)
            return screenshot_path
        finally:
            driver.quit()

    def check_website_status(self, url):
        # Function to check if a website is up (status code 200)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        try:
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def check_waf(self, url):
        # Function to check for the presence of a Web Application Firewall (WAF)
        payload = "/?test=%3Cscript%3Ealert(1)%3C/script%3E"  # Modify this based on your specific payload
        full_url = url + payload
        response = requests.get(full_url)

        if response.status_code == 403:
            return "<span style='color: red;'>A Web Application Firewall (WAF) is likely present and blocking access (403 Forbidden).</span>"
        elif response.ok:
            return "<span style='color: green;'>A Web Application Firewall (WAF) may be present but is not being detected.</span>"
        else:
            return "Unexpected response. Further inspection may be needed."

    def url_to_filename(self, url):
        # Function to convert a URL to a valid filename
        return "".join(c if c.isalnum() else "_" for c in url)

    def generate_html_report(self, results, output_file):
        # Function to generate an HTML report based on the results
        with open(output_file, "w") as file:
            file.write(
                """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Web Check Report</title>
                    <style>
                        body {
                            font-family: 'Helvetica', sans-serif;
                            max-width: 800px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #36454F;  /* Charcoal Grey background */
                            color: white;  /* white text */
                        }
                        h1 {
                            text-align: center;
                        }
                        h2 {
                            border-bottom: 1px solid #ddd;
                            padding-bottom: 5px;
                            margin-top: 20px;
                        }
                        p {
                            margin: 0;
                        }
                        .up {
                            color: green;
                        }
                        .down {
                            color: red;
                        }
                        img {
                            max-width: 100%;
                            height: auto;
                            margin-top: 10px;
                        }
                    </style>
                </head>
                <body>
                    <h1>Web Check Report</h1>
                """
            )

            for url, status, screenshot_path, waf_result in results:
                file.write(f"<h2>{url}</h2>")
                status_text = 'Up' if status else 'Down'
                status_class = 'up' if status else 'down'
                file.write(f"<p>Status: <span class='{status_class}'>{status_text}</span></p>")
                file.write(f"<p>WAF Check: {waf_result}</p>")
                if status:
                    file.write(f'<img src="{screenshot_path}" alt="Screenshot"/>')
                else:
                    file.write("<p>No screenshot available</p>")

            file.write("</body></html>")

    def speak_start_message(self):
        # Function to speak a starting message
        engine = pyttsx3.init()
        engine.say("Web check starting! Please wait.")
        engine.runAndWait()

    def speak_completed_message(self):
        # Function to speak a completion message
        engine = pyttsx3.init()
        engine.say("Web check completed!")
        engine.runAndWait()

    def run_web_scoping(self):
        # Function to run the web scoping checks
        url_or_file = self.entry_url.text()

        if os.path.isfile(url_or_file):
            with open(url_or_file, 'r') as file:
                self.urls = file.read().splitlines()
        else:
            self.urls = [url_or_file]

        output_directory = "screenshots"
        report_file = "web_check_report.html"

        chromedriver_path = r"C:\Users\k3nn3dy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        results = []

        # Get the value of the WAF check toggle
        waf_check_enabled = self.waf_check_toggle.isChecked()

        self.speak_start_message()

        for url in self.urls:
            status = self.check_website_status(url)

            if waf_check_enabled:
                waf_result = self.check_waf(url)
            else:
                waf_result = "WAF check disabled."

            if status:
                screenshot_path = self.take_screenshot(url, output_directory, chromedriver_path)
            else:
                screenshot_path = None

            results.append((url, status, screenshot_path, waf_result))

        self.generate_html_report(results, report_file)
        os.system(report_file)

        self.speak_completed_message()

        print("Web check completed!")

# Main entry point
if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = WebScopingApp()
    window.show()
    app.exec_()
