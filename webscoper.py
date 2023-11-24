"""
****************************************
*          WebScoper by K3nn3dy         *
****************************************
"""

import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from tkinter import Tk, Label, Entry, Button, filedialog
from datetime import datetime

# Function to take a screenshot using Selenium
def take_screenshot(url, output_directory, chromedriver_path):
    options = Options()
    options.add_argument("--headless")

    # Use the specified chromedriver path
    driver_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
    try:
        driver.get(url)
        screenshot_path = os.path.join(output_directory, f"{url_to_filename(url)}.png")
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    finally:
        driver.quit()

# Function to check if a website is up and running
def check_website_status(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Function to convert URL to a filename-friendly format
def url_to_filename(url):
    return "".join(c if c.isalnum() else "_" for c in url)

# Function to generate an HTML report
def generate_html_report(results, output_file):
    with open(output_file, "w") as file:
        file.write("<html><head><title>Web Scoping Report</title></head><body>")
        file.write("<h1>Web Scoping Report</h1>")

        for url, status, screenshot_path in results:
            file.write(f"<h2>{url}</h2>")
            file.write(f"<p>Status: {'Up' if status else 'Down'}</p>")
            if status:
                file.write(f'<img src="{screenshot_path}" alt="Screenshot" width="800"/>')
            else:
                file.write("<p>No screenshot available</p>")

        file.write("</body></html>")

# Function to handle the "Browse" button click event
def browse_file():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    entry_url.delete(0, 'end')
    entry_url.insert(0, file_path)

# Function to handle the "Run Web Scoping" button click event
def run_web_scoping():
    url_or_file = entry_url.get()

    if os.path.isfile(url_or_file):
        with open(url_or_file, 'r') as file:
            urls = file.read().splitlines()
    else:
        urls = [url_or_file]

    output_directory = "screenshots"
    report_file = "web_scoping_report.html"
    
    # Replace this with the path where you downloaded chromedriver
    chromedriver_path = r"C:\Users\k3nn3dy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    results = []

    for url in urls:
        status = check_website_status(url)

        if status:
            screenshot_path = take_screenshot(url, output_directory, chromedriver_path)
        else:
            screenshot_path = None

        results.append((url, status, screenshot_path))

    generate_html_report(results, report_file)

    # Open the generated HTML report in the default web browser
    os.system(report_file)

# GUI setup
root = Tk()
root.title("Web Scoping Tool")

label_url = Label(root, text="Enter URL or Select File:")
label_url.pack(pady=10)

entry_url = Entry(root, width=50)
entry_url.pack(pady=10)

button_browse = Button(root, text="Browse", command=browse_file)
button_browse.pack(pady=10)

button_run_scoping = Button(root, text="Run Web Scoping", command=run_web_scoping)
button_run_scoping.pack(pady=20)

root.mainloop()
