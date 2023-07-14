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

### 1. Prereqs: Install Python and Additional Packages

The program requires that Python and some additional packages already be installed on your local machine. 

#### 1.1 If Python is not installed on your computer

- We recommend installing python using [Anaconda](https://www.anaconda.com/download#downloads). Anaconda is a convenient package manager that will automatically install both python and the required additional packages on to your computer
- Optional: After installing Anaconda, you might find it helpful to view [this free Anaconda tutorial](https://freelearning.anaconda.cloud/get-started-with-anaconda).

#### 1.2 If you are not sure whether Python is installed on your computer

- If you are not sure whether Python is installed, you should assume it is not. Some operating systems (e.g., Macintosh) come with Python preinstalled, but those versions are not easy to access or update. It is preferable to install a fresh version that is easier to use
- Follow the instructions in Section 1.1 above to install Python and the additional packages via Anaconda.

#### 1.3 If Python is already installed your computer

Tour de World uses some packages that are not part of the Python standard library. If you have installed Python using Anaconda, you already have these packages. You are done with the prerequesites and can move on to Section 2.

If you have installed Python without using Anaconda, such as directly from [python.org](https://www.python.org/downloads/), you will need to install the additional packages. Open a command line prompt such as Terminal or PowerShell. Type the following commands at the prompt. Depending on your installation, you many need to substitute `python3` for `python`.

- `python -m pip install -U pip`. This installs the latest version of [pip](https://pypi.org/project/pip/), the Python Package Installer that allows the installation of the other required packages
- `python -m pip install -U requests`. This installs [requests](https://pypi.org/project/requests/), a library that allows Python programs to access web pages and API request via HTTP
- `python -m pip install -U matplotlib`. Matplotlib enables the creation of plots, charts, and other visualizations in Python. Installing matplotlib also automatically installs numpy, the gold standard for scientific calculations in python. Tour de World requires numpy.

### 2. Install Tour de World

Download and intall this entire repo to your local machine. 

- Click on the green Code button above this README
  - If you don't see the button, go to the [main page for this repo](https://github.com/morosebose/countries_data) and try again
- From the menu that opens, choose Download ZIP
- On the local machine, uncompress the ZIP file to a location of your choice

### 3. Run Tour de World

- Open a command line prompt such as Terminal (Mac) or Powershell (Windows).
- At the command prompt, navigate into the folder that you just unzipped: `cd <path/to/unzipped_folder>` (Mac/Linux) or `cd <path\to\unzipped_folder>` (Windows)
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
