'''
Tour de World Front End
Authors: James Kang, Surajit Bose
Copyright © 2023

This project relies on the REST Countries API by Alejandro Matos: 
    - https://restcountries.com/
    - https://gitlab.com/restcountries/restcountries

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at https://mozilla.org/MPL/2.0/
'''


# import modules
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
import sqlite3
import webbrowser
from os.path import exists
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import StrMethodFormatter
import matplotlib.pyplot as plt
import numpy as np

class LanguageDisplayWindow(tk.Toplevel) :
    '''Display the list of countries where a given language has official status'''
    def __init__(self, master, language, countries) :
        super().__init__(master)
        self.title(language)
        
        cols = 2
        num = len(countries)
        if num == 1:
            suffix = 'y'
        else :
            suffix = 'ies'
            if num > 10 :
                cols = 3
  
        display_str = f'{language} is an official language in {num} countr{suffix}'
        
        tk.Label(self, text = display_str, font = ('Calibri', 13, 'bold'), \
                 padx = 10, pady = 10).grid()
        frame = tk.Frame(self)
        i = 0
        j = 0
        for flag, country in countries :
            tk.Label(frame, text = f'{flag} {country}\t\t', fg = 'blue', \
                font = ('Calibri', 12)).grid(sticky = 'W', row = i, column = j)
            j += 1
            if j % cols == 0 :
                i += 1  
                j = 0
        frame.grid(padx = 10, pady = 10)


class CountryCardWindow(tk.Toplevel) :
    '''Class to display individual cards, gets called for every country selected'''
    def __init__(self, master, selected_countries) :
        super().__init__(master)
        self.title('Country Cards')
        self.resizable(False, False)

        # create notebook
        self.card_notebook = ttk.Notebook(self)

        for country in selected_countries:
            name, flag, official, capitals, pop, area, langs, currency, continent, url, code = country
            prompt_str = tk.StringVar()
            prompt_str.set(f'General Information for {name}')
            cap_label = 'Capital'
            if ', ' in capitals :
                cap_label += 's'
            lang_label = 'Language'
            if ', ' in langs :
                lang_label += 's'
            currens_label = 'Currency'
            if ', ' in currency :
                currens_label = 'Currencies'

            # create tab Frame to put into the window
            my_frame1 = tk.Frame(self.card_notebook)
            tk.Label(my_frame1, textvariable = prompt_str, font = ('Calibri', 13)).grid()
            tk.Label(my_frame1, text = flag, font = ('Calibri', 50), fg = 'blue', pady = 20).grid()
            tk.Label(my_frame1, text = official, font = ('Calibri', 14), fg = 'blue').grid()
            tk.Label(my_frame1, text = f'{cap_label}: ' + capitals, font = ('Calibri', 13), fg = 'blue').grid()
            tk.Label(my_frame1, text = f'Population: {pop : ,}', font = ('Calibri', 13), fg = 'blue').grid()
            tk.Label(my_frame1, text = f'Area: {area : ,} km\u00B2', font = ('Calibri', 13), fg = 'blue').grid()
            tk.Label(my_frame1, text = f'{lang_label}: ' + langs, font = ('Calibri', 13), fg = 'blue', wraplength = 250,
                     justify = 'center').grid()
            tk.Label(my_frame1, text = f'{currens_label}: ' + currency.title(), font = ('Calibri', 13), fg = 'blue').grid()
            tk.Label(my_frame1, text = 'Continent: ' + continent, font = ('Calibri', 13), fg = 'blue').grid()
            tk.Button(my_frame1, text = 'Visit on Google Maps', fg = 'blue', font = ('Calibri', 12),
                      command = lambda: webbrowser.open(url)).grid(pady = 20)

            my_frame1.grid()
            my_frame1.grid_columnconfigure(0, weight = 1)

            # adds each tab frame to the Noteboosk
            self.card_notebook.add(my_frame1, text = f'{code}')

        self.card_notebook.grid()

class PlotWindow(tk.Toplevel):
    '''Class to display boxplot and bar chart of area or population'''
    def __init__(self, master, desired, countries, data, bar):
        super().__init__(master)
        
        t_label = 'Area' if desired == 'area' else 'Population'
        plot_title = f'{t_label} of Selected Countries'
        if t_label == 'Area' :
            t_label += ' (km\u00B2)'
                
        if bar :
            fig = plt.figure(figsize = (10, 5))
            plt.title(plot_title)
            plt.xlabel(f'{t_label}', fontsize = 10)
            plt.ylabel('Countries', fontsize = 10)
            plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.barh(countries, data)
            
        else : 
            fig = plt.figure(figsize = (6,4))
            plt.title(f'Box Plot of {plot_title}')
            plt.ylabel(f'{t_label}', fontsize = 10)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.boxplot(data, labels = ['Selected Countries'])
            
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class DialogWindow(tk.Toplevel) :
    '''
    Class to interact with the user and display a listbox for user to get selection of countries
    '''
    def __init__(self, master, desired, prompt, data, mini, maxi, npstr) :
        super().__init__(master)
        self.grab_set()
        self.focus_set()
        self.transient(master)
        self._choice = (-1, )
        
        self.prompt_str =  tk.StringVar()
        self.prompt_str.set(prompt)
        
        self.numpy_str = tk.StringVar()
        self.numpy_str.set(npstr)

        self.minsize(415, 250)
        self.maxsize(550, 300)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        promptFrame = tk.Frame(self)
        tk.Label(promptFrame, textvariable = self.prompt_str, font = ('Calibri', 13)).grid()
        promptFrame.grid()

        listboxFrame = tk.Frame(self)
        how_many = 'single' if desired in ['continent', 'language'] else 'multiple'
        self._lb = tk.Listbox(listboxFrame, height = 8, selectmode = how_many)
        
        if desired != 'continent' :
            self._sb = tk.Scrollbar(listboxFrame, orient = 'vertical', command = self._lb.yview)
            self._lb.config(yscrollcommand = self._sb.set)
            self._sb.grid(row = 1, column = 1, sticky = 'NS')              
            tk.Label(listboxFrame, textvariable = self.numpy_str, font = ('Calibri', 12), pady = 3).grid()
            
        self._lb.insert(tk.END, *data)
        self._lb.grid(row = 1, column = 0, sticky = 'EW')
        self._lb.grid(row = 1, column = 0)
        tk.Button(listboxFrame, text = 'Click to select', command = lambda: self._setChoice(desired, mini, maxi)).grid(row = 3, padx = 5, pady = 10)
        listboxFrame.grid(row = 2, padx = 10, pady = 10)

        self.protocol('WM_DELETE_WINDOW', self.destroy)


    def _setChoice(self, desired, mini, maxi) :
        
        if desired in ['continent', 'language']: 
            err = f'Please choose a {desired}'
        else :
            err = f'Please choose between {mini} and {maxi} countries'
            
        choice = self._lb.curselection()
        
        if not mini <= len(choice) <= maxi :
            tkmb.showerror('Error', err, parent = self)
            self._lb.selection_clear(0, tk.END)
            choice = self._lb.curselection()
        else :
            self._choice = choice
            self.destroy()


    @property
    def chosen(self) :
        return self._choice


class MainWindow(tk.Tk) :
    '''
    OOP implementation of tk.Tk class. 
    - Create root window for application
    - Spawn other windows as needed to display data or get user choice
    '''
    
    # Class attributes
    COUNTRIES_DB = 'countries.db' # database from which window displays data
    MIN_COUNTRIES = 5 # minimum number of countries to display
    MAX_COUNTRIES = 12 # maximum number of countries to display

    def __init__(self) :
        '''
        Create database connection and cursor. Instantiate main window
        with all the widgets.
        '''
        super().__init__()

        if not exists(MainWindow.COUNTRIES_DB)  :
            tkmb.showerror(f'Cannot open {MainWindow.COUNTRIES_DB}', parent = self)
            raise SystemExit
            
        self._conn = sqlite3.connect(MainWindow.COUNTRIES_DB)
        self._curr = self._conn.cursor()

        self.attributes('-topmost', 'true')
        self.title('Tour de World')
        # places the window in the middle of the screen
        self.geometry('350x170+500+500')
        self.minsize(280, 200)
        self.maxsize(470, 270)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)

        # Main title of Application
        titleFrame = tk.Frame(self) # using frame in case we want to add a globe to the background img
        tk.Label(titleFrame, text = 'Tour de World', font = ('Calibri', 20)).grid( pady = 15)
        titleFrame.grid(row = 0)

        # Label to prompt & buttons to lock-in choice
        buttonFrame = tk.Frame(self)
        tk.Label(buttonFrame, text = 'Search Countries Data By : ', font = ('Calibri', 13)).grid(row = 0, columnspan = 3, pady = 10)
        tk.Button(buttonFrame, text = 'Area', command = lambda: self.getContinentChoice('area')).grid(row = 1, column = 0)
        tk.Button(buttonFrame, text = 'Population', command = lambda: self.getContinentChoice('population')).grid(row = 1, column = 1)
        tk.Button(buttonFrame, text = 'Language', command = self._handleLanguage).grid(row = 2, column = 0)
        tk.Button(buttonFrame, text = 'General Info', command = lambda: self.getContinentChoice('general')).grid(row = 2, column = 1)
        buttonFrame.grid(pady = 20)

        self.protocol('WM_DELETE_WINDOW', self.mainWinClose)


    def getContinentChoice(self, desired) :
        '''
        Generate sorted list of appropriate countries based on user choice
        Pass list on to method to get user's choice of countries
        '''       
        self._curr.execute('SELECT name FROM Continents ORDER BY name')
        continents = list(zip(['Worldwide'], *self._curr.fetchall()))[0]
        
        prompt = 'What part of the world would you like to tour?'
        region = self._getChoice('continent', prompt, continents)[0]

        if region == -1 :   # User closed window without choosing
            return        
         
        cmd = self._getCommand(desired, region)   
        if region :     # User chose specific continent
            locale = continents[region]
            locale_str = f'in {locale}'
            self._curr.execute(cmd, (locale,))
        else :
            locale_str = 'Worldwide'
            self._curr.execute(cmd)
            
        data = list(zip(*self._curr.fetchall()))[0]
         
        if desired == 'general' :
            mini = 1
            maxi = MainWindow.MIN_COUNTRIES
            self._handleGeneral(data, locale_str, desired, mini, maxi)
        else :
            mini = MainWindow.MIN_COUNTRIES
            maxi = MainWindow.MAX_COUNTRIES
            self._handleAreaOrPop(data, locale_str, desired, mini, maxi)
    
            
    def _handleAreaOrPop(self, data, locale_str, desired, mini, maxi) :
        '''Get list of countries with population or area data'''
        cont_data = [self._curr.execute(f'''SELECT {desired} from Countries 
                WHERE name = ?''', (country,)).fetchone()[0] for country in data]
        cont_array = np.array(cont_data)
        prompt = f'Select between {mini} and {maxi} countries {locale_str} (sorted by {desired})'
        label_var = f'Total Countries : {len(cont_array)}    Total {desired} : {np.sum(cont_array) : ,} '
        if desired == 'area' :
            label_var += ' km\u00B2'
        choices = self._getChoice(desired, prompt, data, label_var, mini, maxi)
        if choices[0] == -1 :  # user closed without choosing
            return
        self._launchCountries(desired, data, choices)


    def _handleGeneral(self, data, locale_str, desired, mini, maxi) :
        '''Get list of countries with general info'''
        prompt = f'Select between {mini} and {maxi} countries (sorted alphabetically)'
        label_var = f'Total countries {locale_str} : {len(data)}'
        choices = self._getChoice(desired, prompt, data, label_var, mini, maxi)
        if choices[0] == -1 : # user closed without choosing
            return
        self._launchCard(data, choices)
    
    
    def _handleLanguage(self):
        '''
        Generate sorted list of languages
        Get user's choice of language
        Display list of countries where that language is official
        '''
        self._curr.execute('''SELECT name FROM Languages 
                    WHERE name != 'None' ORDER BY name''')
        langs = list(zip(*self._curr.fetchall()))[0]
        prompt = 'Select a language (sorted alphabetically)'
        label_var = f'Number of Official Languages : {len(langs)}'
        choice = self._getChoice('language', prompt, langs, label_var)[0]
        if choice == -1 : # user closed without choosing
            return
        selected = langs[choice]
        self._curr.execute('''SELECT C.flag, C.name FROM Countries C
                    INNER JOIN Count_Lang_Jn CL on C.id = CL.Country
                    INNER JOIN Languages L on CL.language = L.id
                    WHERE L.name = ? ORDER BY C.name''', (selected,))
        countries_list = list(self._curr.fetchall())
        LanguageDisplayWindow(self, selected, countries_list)

        

    def _getCommand(self, desired, region) :
        '''Get approppriate SQL command to run on database depending on user choice'''
        if desired == 'general' :
            if not region :
                # User wants general info worldwide
                return 'SELECT name FROM Countries ORDER BY name'
            # user wants general info for specific region
            return '''SELECT Countries.name FROM Countries JOIN Continents
                    ON Countries.continent = Continents.id
                    WHERE Continents.name = ? 
                    ORDER BY Countries.name'''
        if not region :
            # user wants area or pop info worldwide
            return f'SELECT name from Countries ORDER BY {desired} DESC'
        # user wants area or pop info for specific region
        return f'''SELECT Countries.name FROM Countries JOIN Continents
                ON Countries.continent = Continents.id
                WHERE Continents.name = ? ORDER BY Countries.{desired} DESC'''


    def _getChoice(self, desired, prompt, data, label_var = '', mini = 1, maxi = 1) :
        '''Get user's choice of which continent or countries to see'''
        dwin = DialogWindow(self, desired, prompt, data, mini, maxi, label_var)
        self.wait_window(dwin)
        choice = dwin.chosen
        return choice


    def _launchCountries(self, desired, countries, choices) :
        '''Display chosen countries by area or population'''
        # store countries and data in list to be used for bar chart
        plot_countries = []
        plot_data = []
        # goes through the indices of the curselection of the countries
        for choice in choices :
            plot_countries.append(countries[choice])
            self._curr.execute(f'''SELECT {desired} FROM Countries 
                                    WHERE name = ?''', (countries[choice],))
            plot_data.append(self._curr.fetchone()[0])
            
        for bar in (True, False) : 
            PlotWindow(self, desired, plot_countries, plot_data, bar)


    def _launchCard(self, countries, choices) :
        '''Display general info for individual countries'''
        selected_countries = []
        for choice in choices :
            name = countries[choice]
            self._curr.execute('''SELECT C.flag, C.official, C.population, C.area, CO.name, C.map, C.code
                                    FROM Countries C, Continents CO
                                    WHERE C.continent = CO.id AND C.name = ?''', (name, ))
            flag, official, pop, area, continent, url, code = self._curr.fetchone()
            caps, langs, currens = self._getMultiples(name)
            selected_countries.append((name, flag, official, caps, pop, area, langs, currens, continent, url, code))

        CountryCardWindow(self, selected_countries)
            
    def _getMultiples(self, name) :
        cap_set = set()
        lang_set = set()
        currens_set = set()
        set_list = [cap_set, lang_set, currens_set]
        for result in self._curr.execute('''SELECT CAP.name, L.name, CUR.name
                    FROM Countries C 
                    INNER JOIN Count_Lang_Jn CL on C.id = CL.Country
                    INNER JOIN Languages L on CL.language = L.id
                    INNER JOIN Count_Cap_Jn CC on C.id = CC.Country
                    INNER JOIN Capitals CAP on CC.capital = CAP.id
                    INNER JOIN Count_Curr_Jn CR on C.id = CR.country
                    INNER JOIN Currencies CUR on CR.currency = CUR.id
                    WHERE C.name = ?''', (name, )) :
            for i in range(len(set_list)) :
                set_list[i].add(result[i])
        caps = ', '.join(sorted(cap_set))
        langs = ', '.join(sorted(lang_set))
        currens = ', '.join(sorted(currens_set))
        return caps, langs, currens
    

    def mainWinClose(self) :
        '''
        callback function to quit the program and all memory when user clicks 'X'
        '''
        if tkmb.askokcancel('Confirm close', 'Close all windows and quit?', parent = self) :
            self._conn.close()
            self.destroy()
            self.quit()


if __name__ == '__main__' :
    MainWindow().mainloop()
