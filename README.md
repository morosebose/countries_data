# Countries Database 

This project uses the [REST Countries](https://restcountries.com/) API to create a database of all countries around the world.
The database is linked to a GUI front end that allows users to choose how they want to view the countries' data. The user will also be able to filter the list of all the countries by choosing the whole world or by the 6 continents. For example, the user can choose to display the top five countries by population or by area. Or the user can choose specific countries to view general information about them. 

Information for each country includes:
- Common name, e.g., Suriname
- Official name, e.g.,  Republic of Suriname
- Capital
- Population
- Currency
- Continent, etc. 

## Skills
- Web access, API call, JSON 
- Database CRUD using SQLite
- Data analytics with numpy or pandas
- Display data with matplotlib 
- GUI front end with Tkinter

## Files

To run the program, download and install final_back.py and final_front.py into the same folder/directory on your local machine. First run final_back.py, then run final_front.py from the command line.

- final_back.py has the API call and the code to create the database from the resulting JSON download. This file creates two additional files:
  - area_pop_data.csv a CSV of the numeric (integer) data from the database
  - countries.db a sqlite database of the countries data from the API
- final_front.py has the GUI front end to navigate and display the data using TKinter and numpy

## Credits
- Final project for for CIS 41B (Advanced Python Programming) at De Anza College, Spring 2023
- Professor: Clare Nguyen
- Authors, © 2023: 
  - [James Kang](https://github.com/jcmkang), front end (TKinter, matplotlib) 
  - [Surajit A. Bose](https://github.com/morosebose), back end (JSON, SQLite, numpy/pandas)
- REST Countries API provided by [Alejandro Matos](https://gitlab.com/amatos). 
