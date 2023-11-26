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
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, filedialog, ttk
from datetime import datetime

def take_screenshot(url, output_directory, chromedriver_path):
    options = Options()
    options.add_argument("--headless")

    driver_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
    try:
        driver.get(url)
        screenshot_path = os.path.join(output_directory, f"{url_to_filename(url)}.png")
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    finally:
        driver.quit()

def check_website_status(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def url_to_filename(url):
    return "".join(c if c.isalnum() else "_" for c in url)

def generate_html_report(results, output_file):
    with open(output_file, "w") as file:
        file.write(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Web Scoping Report</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #3498db;  /* Blue background */
                        color: white;  /* White text */
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
                <h1>Web Scoping Report</h1>
            """
        )

        for url, status, screenshot_path in results:
            file.write(f"<h2>{url}</h2>")
            status_text = 'Up' if status else 'Down'
            status_class = 'up' if status else 'down'
            file.write(f"<p>Status: <span class='{status_class}'>{status_text}</span></p>")
            if status:
                file.write(f'<img src="{screenshot_path}" alt="Screenshot"/>')
            else:
                file.write("<p>No screenshot available</p>")

        file.write("</body></html>")

def browse_file():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    entry_url.delete(0, 'end')
    entry_url.insert(0, file_path)

def run_web_scoping():
    url_or_file = entry_url.get()

    if os.path.isfile(url_or_file):
        with open(url_or_file, 'r') as file:
            urls = file.read().splitlines()
    else:
        urls = [url_or_file]

    output_directory = "screenshots"
    report_file = "web_scoping_report.html"
    
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
    os.system(report_file)

# GUI setup
root = Tk()
root.title("Web Scoping Tool")

style = ttk.Style()
style.configure('TButton', padding=(10, 5), font=('Helvetica', 10))
style.configure('TLabel', font=('Helvetica', 12))

# Set background and foreground colors for the root window
root.configure(bg='#3498db')  # Blue background color

label_url = ttk.Label(root, text="Enter URL or Select File:", style='TLabel', background='#3498db', foreground='white')
label_url.pack(pady=10)

entry_url = ttk.Entry(root, width=50)
entry_url.pack(pady=10)

button_browse = ttk.Button(root, text="Browse", command=browse_file)
button_browse.pack(pady=10)

button_run_scoping = ttk.Button(root, text="Run Web Scoping", command=run_web_scoping)
button_run_scoping.pack(pady=20)

# Set the overall window size
root.geometry("400x300")

root.mainloop()
