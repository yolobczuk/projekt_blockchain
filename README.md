# Documentation

## Initial requirements

* Backend - code that creates block and puts it into the simulated blockchain. It also should allow filling the block with data from Flask form.
* Flask - simple form that allows to save ticket data into the blockchain (such as name, surname, pesel [Polish unique identification number], value of ticket, penalty points given [if applicable] as well as name, surname and badge number of police officer that gave the ticket). All sensitive data such as names, surnames, PESEL and badge numbers will be hashed. It should give the possibility of showing tickets for given PESEL or badge number hash. It will also be convienient if the site would have the option to show hash for a specific PESEL/badge id. 
* Database - as it is expensive to put the data into a real blockchain network and it is hard to create your own network, my proposal is that we simulate the blockchain network by creating a conventional database that emulates the structure of blockchain.

## Manual

In order to initialise the database you have to type in bash terminal following commands: flask db init, flask db migrate, flask db upgrade

# Technical documentation

1. Software characteristics
  - Shortened name: Ticketing system
  - Full name: 
  - Description: This app allows to input ticket data into database stored as blockchain.
Every ticket is stored inside a unique block with unique hashcode what allows to keep every
ticket unchanged.
2. Copyright
  - Authors: Jan Jarosz, Mateusz Kacprowicz, Wojciech Sobczuk
  - Licensing:
3. Requirements
| # | Requirement title | Description | Priority | Category |
|:-:|:-----------------:|:-----------:|:--------:|:--------:|
|   |                   |             |          |          |
4. Software architecture
  - Used IDEs: Visual Studio Code, ver. 1.74.2;
  - Used programming languages: Python, ver. 3.9.2
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
5. User tests
