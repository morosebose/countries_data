# Countries Database 

This project uses the [REST Countries](https://restcountries.com/) API to create a database of all the countries around the world. The database is linked to a GUI front-end that allows users to select how they want to view the data of the countries. The users can also choose if they want to view the countries worldwide or by any of the 7 continents. For example, the user can choose to compare the top five countries by population in Europe, or seven countries in South America by area. Or the user can choose specific countries worldwide to view general information about them. 

General information for each country includes:
- Common name, e.g., Suriname
- Official name, e.g.,  Republic of Suriname
- Capital
- Area in square kilometers
- Population
- Currency
- Continent, etc. 

## Skills
- Web access, API call, JSON 
- Database CRUD using SQLite
- Display data with matplotlib 
- GUI front end with Tkinter

## Files
The program requires that python be installed on your local machine. If you do not have python installed, you can download the latest version from [python.org](https://www.python.org/downloads/). 

To run this program, download and install `final_back.py` and `final_front.py` from this repository into a single folder/directory on your local machine. After doing so, use the command line to run each file in this order: first `python final_back.py`, then `python final_front.py`. 

- `final_back.py` has the API call and the code to create the database from the resulting JSON download. This file creates two additional files:
  - `area_pop_data.csv`, a CSV of the numeric (integer) data from the database
  - `countries.db`, a sqlite database of the countries data from the API
- `final_front.py` has the GUI front end to navigate and display the data using TKinter.

## Credits
- Final project for for CIS 41B (Advanced Python Programming) at De Anza College, Spring 2023
- Professor: Clare Nguyen
- Authors, © 2023: 
  - [James Kang](https://github.com/jcmkang), front end (TKinter, matplotlib) 
  - [Surajit A. Bose](https://github.com/morosebose), back end (JSON, SQLite, numpy/pandas)
- REST Countries API provided by [Alejandro Matos](https://gitlab.com/amatos). 
