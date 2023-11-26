# Web Scoping Tool

Web Scoping Tool is a simple application that allows you to check the status of web pages and capture screenshots for a list of URLs.

## Features

- Check the status of web pages to determine if they are up or down.
- Capture screenshots of web pages for further analysis.
- Easy-to-use GUI for inputting URLs or loading them from a file.
- [**IN DEVELOPMENT**] Option to check for the presence of a Web Application Firewall (WAF).

## Requirements

- Python 3.x
- ChromeDriver (download and set the path in the script)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/web-scoping-tool.git

2. Install the required dependencies:

   pip install -r requirements.txt

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

