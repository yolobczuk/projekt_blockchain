# Documentation

## Initial requirements

* Backend - code that creates block and puts it into the simulated blockchain. It also should allow filling the block with data from Flask form.
* Flask - simple form that allows to save ticket data into the blockchain (such as name, surname, pesel [Polish unique identification number], value of ticket, penalty points given [if applicable] as well as name, surname and badge number of police officer that gave the ticket). All sensitive data such as names, surnames, PESEL and badge numbers will be encytped under hashcode. It should give the possibility of showing tickets for given PESEL or badge number hash. It will also be convienient if the site would have the option to show hash for a specific PESEL/badge id. 
* Database - as it is expensive to put the data into a real blockchain network and it is hard to create your own network, my proposal is that we simulate the blockchain network by creating a conventional database that emulates the structure of blockchain.

# Technical documentation

### Software characteristics
  - Shortened name: Ticketing system
  - Full name: Ticketing system with web application and blokchain storage system
  - Description: This app allows to input ticket data into database stored as blockchain.
Every ticket is stored inside a unique block with unique hashcode what allows to keep every
ticket and its data unchanged.

### Copyright
  - Authors: Jan Jarosz, Mateusz Kacprowicz, Wojciech Sobczuk
  - Licensing: This work is licensed under CC BY 4.0. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/

### Requirements

  | # | Requirement title | Description | Priority | Category |
  |:-:|:-----------------:|:-----------:|:--------:|:--------:|
  | 1 | Secure Infrastructure | The ticketing system service must be impenetrable by a bad actor | Priority 1 | Non-functional |
  | 2 | Accessible Service | The ticketing system service must be available from every device connected to the Internet | Priority 1 | Functional |
  | 3 | User Interface | GUI must be clear and simple in order to ensure work efficacy | Priority 2 | Non-functional |
  | 4 | Confidental Data Handling | All sensitive data (such as government IDs) must be encrypted | Priority 1 | Functional |
  | 5 | User Register Feature | User must be registerred to be able to log-in | Priority 1 | Functional |
  | 6 | Log-in Feature | User must be logged-in in order to browse through the application | Priority 1 | Functional |
  | 7 | Hashing | Application should have the option to convert numbers into hashes | Priority 2 | Functional |
  | 8 | Blockchain Filtering | Application must have the option to print out all blocks within the blockchain as well as filtering its contents by specific categories such as government ID and badge ID | Priority 1 | Functional |
  | 9 | Blockchain Filling | Application must have the option to add new tickets to the blockchain | Priority 1 | Functional |
  | 10 | Password Recovery | User should have a possibility to recover forgotten password | Priority 2 | Functional |
  | 11 | Deploy Of Appplication To Cloud Services | Application should be deployed to cloud services | Priority 2 | Functional |
  
### Software architecture
  - Used IDEs: 
      - Visual Studio Code, ver. 1.74.2,
      - PyCharm 2022.1.3 (Community Edition).
  - Used programming languages: 
      - Python, ver. 3.9.2 (including use of Jinja2 template engine, ver. 3.1.2);,
      - HTML, ver. 5 (including use of Boostrap framework, ver. 5.3).
  - Used and required libraries (in Python): 
      - alembic (1.8.1), 
      - autopep8 (2.0.1), 
      - certifi (2022.6.15), 
      - cffi (1.15.1), 
      - charset-normalizer (2.1.0), 
      - cleanco (2.2), 
      - click (8.1.3), 
      - colorama (0.4.6), 
      - cryptography (38.0.4), 
      - Flask (2.2.2), 
      - Flask-Login (0.6.2), 
      - Flask-Migrate (4.0.0), 
      - Flask-SQLAlchemy (3.0.2), 
      - Flask-WTF (1.0.1), 
      - greenlet (2.0.1), 
      - idna (3.3), 
      - importlib-metadata (5.1.0), 
      - itsdangerous (2.1.2), 
      - Jinja2 (3.1.2), 
      - Mako (1.2.4), 
      - MarkupSafe (2.1.1), 
      - numpy (1.23.1), 
      - pandas (1.4.3), 
      - protobuf (3.20.1), 
      - pycodestyle (2.10.0), 
      - pycparser (2.21), 
      - Pygments (2.9.0), 
      - python-dateutil (2.8.2), 
      - pytz (2022.1), 
      - requests (2.28.1), 
      - sasoptpy (1.0.5), 
      - saspy (4.3.1), 
      - six (1.16.0), 
      - SQLAlchemy (1.4.45), 
      - swat (1.11.0), 
      - tomli (2.0.1), 
      - urllib3 (1.26.10), 
      - Werkzeug (2.2.2), 
      - WTForms (3.0.1), 
      - zipp (3.11.0)
  - Version control system: git version 2.25.1.windows.1
  - Cloud Deployment: Google Cloud Platform
      - Service: Compute Engine - Virtual Machine
      - Instance: 
      - HTTP traffic serving: Nginx
      - Aplication hosting: uWSGI
  - All codes and files are stored on https://github.com/yolobczuk/projekt_blockchain

### Launch architecture
In order to launch the application, Python 3.9.2 with compatible IDE and following libraries are required (versions are listed in the Software architecture part):
  - Flask
  - Flask-SQLAlchemy
  - Flask-Migrate
  - Flask-Login
  - security module from Werkzeug library
  - hashlib
  - datetime
  - json
  - Flask-WTF
  - WTForms (with validator module)

Launching process is different for local and cloud deployment. To access cloud production version, the user must type in '' in the browser search tab. In order to access local production version, the user has to launch the application in the IDE and then navigate to 127.0.0.1:8080 address. In order to access the local debug version of the app, following steps must be taken:
- in the bash terminal, type in following commands: export FLASK_APP=blockchain.py; export FLASK_DEBUG=True; flask run
- navigate to 127.0.0.1:5000 address.

If the user doesn't have the database locally, following commands must be typed into the bash terminal: flask db init; flask db migrate; flask db upgrade.

### User tests
