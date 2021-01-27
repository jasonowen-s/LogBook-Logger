Logbook Logger
=============
Logbook filling automation for [Binus industry site](https://industry.socs.binus.ac.id/learning-plan/). Quickly fill your daily logs via command line and let Selenium do the waiting, typing, clicking and checking. Logbook Logger will recognize national holidays and fill your logbook with the name of the holiday. 
<br /><br /><br />

## Requirements
- [Python 3](https://www.python.org/download/releases/3.0/) (make sure it's added to PATH)
- [Chrome](https://www.google.com/chrome/)
- [Chrome WebDriver](https://chromedriver.storage.googleapis.com/index.html) (version must match your Chrome version, must be added to PATH)
- [Selenium](https://pypi.org/project/selenium/)
```
pip install -U selenium
```
- [Pytanggalmerah](https://pypi.org/project/Pytanggalmerah/)
```
pip install Pytanggalmerah
```
<br /><br />

## Usage Scenarios
### Initial Run
- At first, it will ask for your Binus Industry credentials (will be saved locally as raw text in .json file)
- Then it will ask for basic repetitive info such as clock in and out time along with weekend activity
### Workdays
- You will be prompted for the today's activity and description
- Sip your coffee and go about your day as Logbook Logger logs you in, fills the log and see if everything looks good
### Weekends
- It will automatically fill everything in as defined in the initial run
### National Holidays
- It will check what the holiday is, then fill the logbook accordingly
<br /><br /><br />

## How to Run
### Windows
- Open the run.bat file, and you're good to go
### Mac or Linux
- Run the **logger_script.py** with Python3
```
python3 logger_script.py
```
<br /><br />

## What it Looks Like
### Headless
![headless](assets/headless.gif)
<br /><br />

### With Browser
![with-browser](assets/with-browser.gif)