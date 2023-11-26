# Web Scoping Tool

# Web Checking Tool

The **Web Checking Tool** is a Python-based application that allows users to perform comprehensive checks on web URLs. The tool provides the ability to:

- **Check Website Status:** Verify whether a website is up and running by examining the HTTP status code.

- **Web Application Firewall (WAF) Detection:** Detect the presence of a Web Application Firewall by sending a test payload and analyzing the response.

- **Take Screenshots:** Capture screenshots of websites to visually inspect their appearance.

- **Generate HTML Reports:** Generate detailed HTML reports summarizing the results of the checks.

- **User-Friendly GUI:** The tool features a user-friendly graphical user interface (GUI) built using PyQt5, providing an intuitive experience for users.

- **Speech Feedback:** Receive audible feedback at the start and end of the web checking process using text-to-speech functionality.

This tool is designed to assist users in conducting web scoping activities, ensuring websites are accessible, secure, and free from common vulnerabilities.

## Getting Started

To get started, simply clone the repository and run the application. Follow the on-screen instructions to input URLs, enable/disable checks, and review the generated reports.


## Requirements

- Python 3.x
- ChromeDriver (download and set the path in the script) 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/web-scoping-tool.git

2. Install the required dependencies:
```
   pip install -r requirements.txt
```
3. Install ChromeDriver requried to take headless screenshotes - https://chromedriver.chromium.org/downloads 

Change the line in the code below to point to where you installed the chrome driver

E.g.
```
    chromedriver_path = r"C:\Users\k3nn3dy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

```

## Usage
Run the script:

```
python web_scoping_tool.py
```
Enter the URL or select a file containing a list of URLs.

![image](https://github.com/d1r3w0lf81/WebScoper/assets/65041560/15e56e2e-e0f4-45ca-8b21-5b35d46ef503)


Optionally, select Browse and select a text file with URLs, one per per line must have http or https prefix

Click "Run Web Scoping" to start the process.

Results and screenshots will be saved in the screenshots folder, html page is created and the screenshots displayed with a status.

![image](https://github.com/d1r3w0lf81/WebScoper/assets/65041560/252f427e-e88c-43f3-9a60-d02aebb74a3b)

