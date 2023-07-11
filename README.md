# Tour de World

This project uses the [REST Countries](https://restcountries.com/) API to create a database of all the countries around the world. The database is linked to a GUI front-end that allows users to select how they want to view the data of the countries. The users can also choose if they want to view the countries worldwide or by any of the 7 continents. For example, the user can choose to compare the top five countries by population in Europe, or any nine countries in worldwide by area. Or the user can choose four specific countries in south America to view general information about them. 

General information for each country includes:

- Common name, e.g., Suriname
- Official name, e.g.,  Republic of Suriname
- Capital
- Area in square kilometers
- Population
- Currency
- Official languages
- Continent 

## Code Features

- Web access, API call, JSON 
- Database CRUD using SQLite
- Data display with matplotlib 
- GUI front end with Tkinter

## Program Files

This repo consists of the following files: 

- This README file has general information about the program
- `tour_de_world.py` is the main file to run the program
- `backend.py` has the API call and the code to create the database from the resulting JSON download. Running this file creates `countries.db`, a sqlite database of the countries data from the API
- `frontend.py` has the GUI front end to navigate and display the data using TKinter. This file relies on the existence of `countries.db` in the same directory
- `CODEOWNERS` specifies the authors of the program who have permission to modify the code in this repo
- `LICENSE` provides licensing information.

## Installing and Running the Program

### 1. Install Python

The program requires that Python and some additional packages already be installed on your local machine. To check whether you have Python installed:

- Open a command line prompt such as Terminal, PowerShell, or cmd
- Type `which python` at the prompt. If you see a response such as `/usr/bin/python`, Python is installed on your machine
- If you get an error such as `python not found`, type `which python3`
- If you get the same error, you do not have Python installed. You can download the latest version of Python from [python.org](https://www.python.org/downloads/).

### 2. Install additional libraries

After installing Python, you will need to add the following libraries:

- requests
- matplotlib

To install them, open a command line prompt such as Terminal, PowerShell, or cmd. pyType the following commands at the prompt. Depending on your installation, you many need to substitute `python3` for `python`.  

- `python -m pip install -U pip`. This installs the latest version of [pip](https://pypi.org/project/pip/), the Python Package Installer that allows the installation of the other required packages
- `python -m pip install -U requests`. This installs [requests](https://pypi.org/project/requests/), a library that allows Python programs to access web pages and API request via HTTP
- `python -m pip install -U matplotlib`. Matplotlib enables the creation of plots, charts, and other visualizations in Python.

### 3. Install Countries Database

Download and intall this entire repo to your local machine. 

- Click on the green Code button above this README
  - If you don't see the button, go to the [main page for this repo](https://github.com/morosebose/countries_data) and try again
- From the menu that opens, choose Download ZIP
- On the local machine, uncompress the ZIP file to a location of your choice
- At the command prompt (Terminal, PowerShell, or cmd), navigate into the folder that you just unzipped:
  `cd <path/to/unzipped_folder>` (Mac/Linux) or `cd <path\to\unzipped_folder>` (Windows)
- Once you are in the correct directory, run `python tour_de_world.py` or `python3 tour_de_world.py` as appropriate for your system.

## License
This Source Code Form is subject to the terms of the [Mozilla Public License, v. 2.0](https://github.com/morosebose/countries_data/blob/main/LICENSE). If a copy of the MPL was not distributed with this file, you can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).

## Credits
- Final project for for CIS 41B (Advanced Python Programming) at De Anza College, Spring 2023
- Professor: Clare Nguyen
- Authors, © 2023: 
  - [James Kang](https://github.com/jcmkang), front end (TKinter, matplotlib) 
  - [Surajit A. Bose](https://github.com/morosebose), back end (JSON, SQLite, numpy/pandas)
- [REST Countries API](https://gitlab.com/restcountries/restcountries) provided by [Alejandro Matos](https://gitlab.com/amatos). 
