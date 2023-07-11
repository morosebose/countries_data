'''
Countries Data Front End
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


class DisplayWindow(tk.Toplevel) :
    '''Class to display individual cards, gets called for every country selected'''
    def __init__(self, master, name, flag, official, capitals, pop, area, langs, currency, continent, url) :
        super().__init__(master)       
        self.prompt_str =  tk.StringVar()
        self.prompt_str.set(f'General Information for {name}')
        
        cap_label = 'Capital'
        if ', ' in capitals :
            cap_label += 's'
        lang_label = 'Language'
        if ', ' in langs :
            lang_label += 's'
        currens_label = 'Currency'
        if ', ' in currency :
            currens_label = 'Currencies'

        # make frame, labels, and button for country card
        F = tk.Frame(self)
        tk.Label(F, textvariable = self.prompt_str, font = ('Calibri', 13), padx = 10, pady = 10).grid(columnspan = 2)
        tk.Label(F, text = flag, font = ('Calibri', 14), fg = 'blue').grid(row = 1, column = 0, sticky = 'e')
        tk.Label(F, text = official, font = ('Calibri', 14), fg = 'blue').grid(row = 1, column = 1, sticky = 'w')
        tk.Label(F, text = f'{cap_label}: ' + capitals, font = ('Calibri', 13), fg = 'blue').grid(row = 2, columnspan = 2)
        tk.Label(F, text = f'Population: {pop : ,}', font = ('Calibri', 13), fg = 'blue').grid(row = 3, columnspan = 2)
        tk.Label(F, text = f'Area: {area : ,} km\u00B2', font = ('Calibri', 13), fg = 'blue').grid(row = 4, columnspan = 2)
        tk.Label(F, text = f'{lang_label}: ' + langs, font = ('Calibri', 13), fg = 'blue').grid(row = 5, columnspan = 2)
        tk.Label(F, text = f'{currens_label}: ' + currency.title(), font = ('Calibri', 13), fg = 'blue').grid(row = 6, columnspan = 2)
        tk.Label(F, text = 'Continent: ' + continent, font = ('Calibri', 13), fg = 'blue').grid(row = 7, columnspan = 2)
        F.grid(pady = 20, padx = 10)
        tk.Button(self, text = 'Visit on Google Maps', fg = 'blue', font = ('Calibri', 12), command = lambda : webbrowser.open(url)).grid(padx = 5, pady = 10)


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
    def __init__(self, master, prompt, data, mini, maxi, npstr) :
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
        tk.Label(promptFrame, textvariable = self.prompt_str, font=('Calibri', 13)).grid()
        promptFrame.grid()

        listboxFrame = tk.Frame(self)
        self._lb = tk.Listbox(listboxFrame, height = 8)

        if npstr:
            self._sb = tk.Scrollbar(listboxFrame, orient = 'vertical', command = self._lb.yview)
            self._lb.config(selectmode = 'multiple', yscrollcommand = self._sb.set)
            self._sb.grid(row = 1, column = 1, sticky = 'NS')      
            tk.Label(listboxFrame, textvariable = self.numpy_str, font=('Calibri', 12), pady = 3).grid()

            
        self._lb.insert(tk.END, *data)
        self._lb.grid(row = 1, column = 0, sticky = 'EW')
        self._lb.grid(row = 1, column = 0)
        tk.Button(listboxFrame, text = 'Click to select', command = lambda: self._setChoice(mini, maxi)).grid(row = 3, padx = 5, pady = 10)
        listboxFrame.grid(row = 2, padx = 10, pady = 10)

        self.protocol('WM_DELETE_WINDOW', self.destroy)


    def _setChoice(self, mini, maxi) :
        choice = self._lb.curselection()

        if mini == maxi: 
            err = 'Please make a selection'
        else :
            err = f'Please choose between {mini} and {maxi} countries'
        
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
        tk.Label(titleFrame, text = 'Tour de World', font=('Calibri', 20)).grid( pady = 15)
        titleFrame.grid(row = 0)

        # Label to prompt & buttons to lock-in choice
        buttonFrame = tk.Frame(self)
        tk.Label(buttonFrame, text = 'Search Countries Data By : ', font=('Calibri', 13)).grid(row = 0, columnspan = 3, pady = 10)
        tk.Button(buttonFrame, text = 'Area', command = lambda: self.getContinentChoice('area')).grid(row = 1, column = 0)
        tk.Button(buttonFrame, text = 'Population', command = lambda: self.getContinentChoice('pop')).grid(row = 1, column = 1)
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
        region = self._getChoice(prompt, continents)[0]

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
        
        desired_str = desired if desired == 'area' else 'population'
        mini = MainWindow.MIN_COUNTRIES
        maxi = MainWindow.MAX_COUNTRIES
        
        if desired != 'general' :
            mini = MainWindow.MIN_COUNTRIES
            maxi = MainWindow.MAX_COUNTRIES
            self._handleAreaOrPop(data, locale_str, desired, desired_str, mini, maxi)
        else :
            mini = 1
            maxi = MainWindow.MIN_COUNTRIES
            self._handleGeneral(data, locale_str, desired, desired_str, mini, maxi)
    
            
    def _handleAreaOrPop(self, data, locale_str, desired, desired_str, mini, maxi) :
        '''Get list of countries with population or area data'''
        cont_data = [self._curr.execute(f'''SELECT {desired} from Countries 
                WHERE name = ?''', (country,)).fetchone()[0] for country in data]
        cont_array = np.array(cont_data)
        prompt = f'Select between {mini} and {maxi} countries {locale_str} (sorted by {desired_str})'
        label_var = f'Total Countries : {len(cont_array)}    Total {desired_str} : {np.sum(cont_array) : ,} '
        if desired == 'area' :
            label_var += ' km\u00B2'
        choices = self._getChoice(prompt, data, label_var, mini, maxi)
        if choices[0] == -1 :  # user closed without choosing
            return
        self._launchCountries(desired, data, choices)


    def _handleGeneral(self, data, locale_str, desired, desired_str, mini, maxi) :
        '''Get list of countries with general info'''
        prompt = f'Select between {mini} and {maxi} countries {locale_str} (sorted alphabetically)'
        label_var = ''
        choices = self._getChoice(prompt, data, label_var, mini, maxi)
        if choices[0] == -1 : # user closed without choosing
            return
        self._launchCard(data, choices)
    
    
    def _handleLanguage(self):
        '''
        Generate sorted list of languages
        Get user's choice of language
        Display list of countries where that language is spoken
        '''
        self._curr.execute('SELECT name FROM Languages ORDER BY name')
        langs = list(zip(*self._curr.fetchall()))[0]
        prompt = 'Select a language (sorted alphabetically)'
        label_var = f'Total Languages : {len(langs)}'
        choice = self._getChoice(prompt, langs, label_var)[0]
        if choice == -1 : # user closed without choosing
            return
        selected = langs[choice]
        self._curr.execute('''SELECT C.name FROM Countries C
                    INNER JOIN Count_Lang_Jn CL on C.id = CL.Country
                    INNER JOIN Languages L on CL.language = L.id
                    WHERE L.name = ?''', (selected,))
        countries_list = list(zip(*self._curr.fetchall()))[0]
        num = len(countries_list)
        
        if num == 1:
            suffix = 'y'
        else :
            suffix = 'ies'
            
        if selected == 'None' :
            selected = 'No language'
            
        display_str = f'{selected} is spoken in {num} countr{suffix}: \n'
        for country in countries_list :
            display_str += f'    • {country}\n'
        tkmb.showinfo(choice, display_str, parent = self)
        

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


    def _getChoice(self, prompt, data, label_var = '', mini = 1, maxi = 1) :
        '''Get user's choice of which continent or countries to see'''
        dwin = DialogWindow(self, prompt, data, mini, maxi, label_var)
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
        for choice in choices :
            name = countries[choice]
            self._curr.execute('''SELECT C.flag, C.official, C.pop, C.area, CO.name, C.map 
                                    FROM Countries C, Continents CO
                                    WHERE C.continent = CO.id AND C.name = ?''', (name, ))
            flag, official, pop, area, continent, url = self._curr.fetchone()
            caps, langs, currens = self._getMultiples(name)

            DisplayWindow(self, name, flag, official, caps, pop, area, langs, currens, continent, url)
            
            
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
        caps = ', '.join(cap_set)
        langs = ', '.join(lang_set)
        currens = ', '.join(currens_set)
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
