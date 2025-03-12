Project Name : HAPPYFOX
============

Overview
--------
standalone Python script that integrates with Gmail API and performs some rule based operations on emails.
Example:
This project is a simple email processing system that Reads the  emails  and stores them in a database, and process them based on some conditions.

Installation
------------

Example:
1. Clone the repository:
   git clone https://github.com/sindhudh/HappyFox.git

2. Install dependencies:
   pip install -r requirements.txt

Usage
-----

Example:
1. Run the script:
    1. To fetch and store emails from Gmail:
        python main.py --provider gmail --fetch_emails True
    2. To fetch emails from Gmail and also process them:
        python main.py --provider gmail --fetch_emails True --process_emails True
    3. To just process emails without fetching:
        python fetch_and_process_emails.py --provider gmail --process_emails True
   Note: When you run the scripts for first time or token is expired, it will ask you to authenticate via google single-sign-on,select the google account and continue to give access to application to access your mail box

2. You can also run the test suite:
   cd to test foalder
   pytest

Configuration
-------------
1. Place the email auth credentials downloaded from Google Cloud in configs/credentials.txt
2. Place the application Configuration in app_config.txt
3. Place the rules from processing the email in rules.json





Contact Information
-------------------
For any questions, reach out to sindhudh7@gmail.com.
