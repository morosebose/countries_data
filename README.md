# countries_data

This project uses the [REST Countries](https://restcountries.com/) API to create a database of countries. Information for each country includes:
- Common name, e.g., Suriname
- Official name, e.g.,  Republic of Suriname
- Capital
- Population
- Currency
- Continent, etc. 

The database is linked to a GUI front end that allows users to choose what data they want to view. For example, the user can choose to display the top five countries by population or by area. Or the user can choose specific countries to view general information about them. 

## Skills
- Web access, API call, JSON 
- Database CRUD using SQLite
- Data analytics with numpy or pandas
- Display data with matplotlib 
- GUI front end with Tkinter

## Files
- final_back.py has the API call and the code to create the database from the resulting JSON download. This file creates two additional files:
  - area_pop_data.csv a CSV of the numeric (integer) data from the database
  - countries.db a sqlite database of the countries data from the API
- final_frontier.py has the GUI front end to navigate and display the data using TKinter and numpy

## Credits
- Final project for for CIS 41B (Advanced Python Programming) at De Anza College, Spring 2023
- Professor: Clare Nguyen
- Authors, © 2023: 
  - [James Kang](https://github.com/jcmkang), front end (TKinter, matplotlib) 
  - [Surajit A. Bose](https://github.com/morosebose), back end (JSON, SQLite, numpy/pandas)
- REST Countries API provided by [Alejandro Matos](https://gitlab.com/amatos). 
