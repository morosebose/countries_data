'''
CIS 41B Spring 2023
Surajit A. Bose, James Kang
Final Project Back End
'''
import requests
import sqlite3
import csv

API_URL = 'https://restcountries.com/v3.1/all'
DATABASE = 'countries.db'


def createTables(cur) :  
    '''Download data from API and create database tables'''
    # Create Continents table, many countries in a continent
    # API assigns single continent for each country, even Russia, Turkey, etc
    cur.execute('DROP TABLE IF EXISTS Continents')
    cur.execute('''CREATE TABLE Continents(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT UNIQUE ON CONFLICT IGNORE)''')
            
    # Create Countries table
    cur.execute('DROP TABLE IF EXISTS Countries')
    cur.execute('''CREATE TABLE Countries(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT NOT NULL UNIQUE,
        official TEXT NOT NULL UNIQUE,
        code TEXT NOT NULL UNIQUE,
        indep INTEGER NOT NULL,
        flag TEXT NOT NULL UNIQUE,
        continent INTEGER NOT NULL,
        area INTEGER NOT NULL,
        pop INTEGER NOT NULL,
        map TEXT NOT NULL UNIQUE)''')
    
    # Create Capitals table, one country can have many capitals (South Africa)
    # One capital can serve many countries (Jerusalem for Israel and Palestine)
    cur.execute('DROP TABLE IF EXISTS Capitals')
    cur.execute ('''CREATE TABLE Capitals(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT NOT NULL UNIQUE ON CONFLICT IGNORE)''')
        
    # Create Languages table, many languages in a country
    # Many countries share a language, e.g., Arabic
    cur.execute('DROP TABLE IF EXISTS Languages')
    cur.execute('''CREATE TABLE Languages(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT UNIQUE ON CONFLICT IGNORE)''')
    
    # Create Currencies table, many countries use Euro
    # Some countries officially allow other countries' currencies 
    # alongside their own
    cur.execute('DROP TABLE IF EXISTS Currencies')
    cur.execute('''CREATE TABLE Currencies(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name TEXT NOT NULL UNIQUE ON CONFLICT IGNORE)''')
    
    # Create Count_Cap_Jn table
    cur.execute('DROP TABLE IF EXISTS Count_Cap_Jn')
    cur.execute('''CREATE TABLE Count_Cap_Jn(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        country INTEGER,
        capital INTEGER)''')
    
    # Create Count_Lang_Jn table
    cur.execute('DROP TABLE IF EXISTS Count_Lang_Jn')
    cur.execute('''CREATE TABLE Count_Lang_Jn(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        country INTEGER,
        language INTEGER)''')
    
    # Create Count_Curr_Jn table
    cur.execute('DROP TABLE IF EXISTS Count_Curr_Jn')
    cur.execute('''CREATE TABLE Count_Curr_Jn(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        country INTEGER,
        currency INTEGER)''')
    
    # Create Borders table
    cur.execute('DROP TABLE IF EXISTS Borders')
    cur.execute('''CREATE TABLE Borders(
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        country_1 INTEGER,
        country_2 INTEGER)''')
    

def writeTables (countries, cur) :
    '''Write data from database into tables'''
    # Can't put country into borders table if it isn't in countries table
    # But the countries bordering a given country might not already be there
    # Local dictionary to solve this chicken-and-egg problem
    borders_dict = {}
        
    # Walk through JSON and populate database
    for val in countries :
        country = val['name']['common']
        
        # Prepare to handle special cases before attempting to write tables
        # Or writing will crash / tables will have wrong data
    
        # API has wrong map for Indonesia, shows Hungary?!
        if country == 'Indonesia' :
            map_url = 'https://goo.gl/maps/w7M4eCTtCuFdSnJx9'
        else : 
            map_url = val['maps']['googleMaps']
            
        # API has wrong area for Svalbard and Jan Mayen, shows -1
        if country == 'Svalbard and Jan Mayen' :
            area = 61399
        else :
            area = val['area']
                  
        # Kosovo has no key ['independent']
        try : 
            indep = 1 if val['independent'] else 0
        except KeyError :
            indep = 1      # Most UN Nations recognize Kosovo's independence
     
        # Antarctica, Bouvet Island, Macau, and Heard Island and McDonald 
        # Islands have no capitals, languages, and/or currency
        no_val = ['None']
        
        try :
            caps = val['capital']
        except KeyError :
            caps = no_val
            
        try :
            langs = val['languages'].values()
        except KeyError :
            langs = no_val
            
        try :
            currens = [key['name'] for key in val['currencies'].values()]
        except KeyError :
            currens = no_val
            
        # Island nations have no key ['borders']
        try :
            borders_dict[country] = val['borders']
        except KeyError :
            borders_dict[country] = no_val
        
        # Populate Continents table
        cur.execute('INSERT INTO Continents (name) VALUES (?)', \
                    (val['continents'][0],))
        cur.execute('SELECT id FROM Continents WHERE name = ?', \
                    (val['continents'][0],))
        cont_id = cur.fetchone()[0]

        # Populate Countries table
        cur.execute('''INSERT INTO Countries (name, official, code, 
                    indep, flag, continent, area, pop, map) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                    (country, val['name']['official'], val['cca3'], \
                     indep, val['flag'], cont_id, area, \
                    val['population'], map_url))
        cur.execute('SELECT id FROM Countries WHERE name = ?', (country,))
        cid = cur.fetchone()[0]
        
        # Populate remaining tables including junction tables
        writeOthers(cur, cid, caps, 'Capitals', 'Count_Cap_Jn', 'capital')
        writeOthers(cur, cid, langs, 'Languages', 'Count_Lang_Jn', 'language')
        writeOthers(cur, cid, currens, 'Currencies', 'Count_Curr_Jn', 'currency')
    
    # Populate Borders table
    writeBorders(cur, borders_dict, no_val)
    
    
def writeBorders(cur, borders_dict, no_val) :
    '''Write Borders table'''
    for nation, borders in borders_dict.items() :
        if borders != no_val :
            cur.execute('''SELECT id FROM Countries 
                    WHERE name = ?''', (nation,))
            cid = cur.fetchone()[0]
            for border in borders :
                cur.execute('''SELECT id FROM Countries 
                            WHERE code = ?''', (border,))
                bid = cur.fetchone()[0]
                cur.execute('''INSERT INTO Borders (country_1, country_2)
                            VALUES (?, ?)''', (cid, bid))
            

def writeOthers (cur, country_id, some_list, tab1, tab2, desc) :
    '''Helper function to write many-to-many tables'''
    for item in some_list :
        cur.execute(f'INSERT INTO {tab1} (name) VALUES (?)', (item,))
        cur.execute(f'SELECT id FROM {tab1} WHERE name = ?', (item,))
        current_id = cur.fetchone()[0]
        cur.execute(f'''INSERT INTO {tab2} (country, {desc})
                    VALUES (?, ?)''', (country_id, current_id))


def writeCSV (cur):
    '''Write out CSV of data for numpy use (we ended up not using this)'''
    with open ('area_pop_data.csv', 'w', newline = '') as datafile :
        cur.execute ('SELECT id, continent, area, pop FROM Countries')
        rows = cur.fetchall()
        writer = csv.writer(datafile)
        writer.writerows(rows)
        

def main () :
    '''Code driver'''
    countries = requests.get(API_URL).json()
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    createTables(cur) 
    writeTables(countries, cur)
    conn.commit()
    writeCSV(cur)
    conn.close()


if __name__ == '__main__' :
    main()
