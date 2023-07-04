'''
CIS 41B Spring 2023
James Kang, Surajit Bose
Final Project Front End
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
        
        self.transient(master)
        self.promptStr = tk.StringVar()
        self.promptStr.set(f'General Information for {name}')
        
        cap_label = 'Capital'
        if ', ' in capitals :
            cap_label += 's'
        lang_label = 'Language'
        if ', ' in langs :
            lang_label += 's'
        if ', ' in currency :
            currens_label = 'Currencies'
        else :
            currens_label = 'Currency'

        # make frame, labels, and button for country card
        F = tk.Frame(self)
        tk.Label(F, textvariable = self.promptStr, font = ('Calibri', 13), padx = 10, pady = 10).grid(columnspan = 2)
        tk.Label(F, text = flag, font = ('Calibri', 14), fg = 'blue').grid(row = 1, column = 0, sticky = 'e')
        tk.Label(F, text = official, font = ('Calibri', 14), fg = 'blue').grid(row = 1, column = 1, sticky = 'w')
        tk.Label(F, text = f'{cap_label}: ' + capitals, font = ('Calibri', 13), fg = 'blue').grid(row = 2, columnspan = 2)
        tk.Label(F, text = f'Population: {pop : ,}', font = ('Calibri', 13), fg = 'blue').grid(row = 3, columnspan = 2)
        tk.Label(F, text = f'Area: {area : ,} km\u00B2', font = ('Calibri', 13), fg = 'blue').grid(row = 4, columnspan = 2)
        tk.Label(F, text = f'{lang_label} : ' + langs, font = ('Calibri', 13), fg = 'blue').grid(row = 5, columnspan = 2)
        tk.Label(F, text = f'{currens_label} : ' + currency.title(), font = ('Calibri', 13), fg = 'blue').grid(row = 6, columnspan = 2)
        tk.Label(F, text = 'Continent: ' + continent, font = ('Calibri', 13), fg = 'blue').grid(row = 7, columnspan = 2)
        F.grid(pady = 20, padx = 10)
        tk.Button(self, text = 'Visit on Google Maps', fg = 'blue', font = ('Calibri', 11), command = lambda : webbrowser.open(url)).grid(padx = 5, pady = 10)


class PlotWindow(tk.Toplevel):
    '''Class to display boxplot and bar chart of area or population'''
    def __init__(self, master, desired, continent, data, bar = False):
        super().__init__(master)
        
        t_label = 'Area' if desired == 'area' else 'Population'
                
        country = []
        data_val = []
        for item in data.items() :
            country.append(item[0]), data_val.append(item[1])

        if bar :
            fig = plt.figure(figsize = (10, 5))
            plt.title(f'{t_label} of Selected Countries')
            if t_label == 'Area' :
                t_label += ' (km\u00B2)'
            plt.xlabel(f'{t_label}', fontsize = 10)
            plt.ylabel('Countries', fontsize = 10)
            plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.barh(country, data_val)
            
        else : 
            fig = plt.figure(figsize = (6,4))
            plt.title(f'Box Plot of {t_label} for Selected Countries')
            plt.xlabel('Selected Countries', fontsize = 10)
            if t_label == 'Area' :
                t_label += ' (km\u00B2)'
            plt.ylabel(f'{t_label}', fontsize = 10)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.yticks = (np.min(data_val), np.quantile(data_val, 0.25), \
                np.median(data_val), np.quantile(data_val, 0.75), np.max(data_val))
            plt.boxplot(data_val)
            
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class DialogWindow(tk.Toplevel) :
    '''
    Class to interact with the user and display a listbox for user to get selection of countries
    '''
    def __init__(self, master, prompt, data, mini, maxi, npstr, multi = False) :
        super().__init__(master)
        self.grab_set()
        self.focus_set()
        self.transient(master)
        self._choice = (-1, )

        self.promptStr = tk.StringVar()
        self.promptStr.set(prompt)
        self.numpyStr = tk.StringVar()
        tk.Label(self, textvariable = self.promptStr, font = ('Calibri', 13), padx = 10,
                 pady = 10).grid()

        frame = tk.Frame(self)
        self._sb = tk.Scrollbar(frame, orient = 'vertical')
        if multi :
            self.numpyStr.set(npstr)
            tk.Label(self, textvariable = self.numpyStr, font = ('Calibri', 12), padx = 10, pady = 3).grid()
            self._lb = tk.Listbox(frame, height = 6, selectmode = 'multiple', yscrollcommand = self._sb.set)
        else :
            self._lb = tk.Listbox(frame, height = 6, yscrollcommand = self._sb.set)
        self._sb.config(command = self._lb.yview)
        self._lb.grid(row = 1, column = 0)
        self._sb.grid(row = 1, column = 1, sticky = 'NS')
        frame.grid(row = 2, column = 0, padx = 10, pady = 10)
        self._lb.insert(tk.END, *data)
        tk.Button(self, text = 'Click to select', command = lambda : self._setChoice(mini, maxi)).grid(padx = 5, pady = 10)

        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def _setChoice(self, mini, maxi) :
        choice = self._lb.curselection()
        if not mini <= len(choice) <= maxi :
            tkmb.showerror('Error', f'Please choose between {mini} and {maxi} countries', parent = self)
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

        self.display_windows = []
        self.title('Tour de World')
        # places the window in the middle of the screen
        self.geometry('+500+500')
        # Main title of Application
        tk.Label(self, text = 'Tour de World', font = ('Calibri', 15)).grid(pady = 5)

        # Label to prompt & buttons to lock in choice
        tk.Label(self, text = 'Search Countries Data By  :', font = ('Calibri', 13)).grid(pady = 3)
        buttonFrame = tk.Frame(self)
        tk.Button(buttonFrame, text = 'Area', command = lambda : self.getContinentChoice('area')).grid(row = 2, column = 0)
        tk.Button(buttonFrame, text = 'Population', command = lambda : self.getContinentChoice('pop')).grid(row = 2, column =  1)
        tk.Button(buttonFrame, text = 'General Info', command = lambda : self.getContinentChoice('general')).grid(row = 2,column = 2)
        buttonFrame.grid(pady = 3)

        self.protocol('WM_DELETE_WINDOW', self.mainWinClose)


    def getContinentChoice(self, desired) :
        '''
        Generate sorted list of appropriate countries based on user choice
        Pass list on to method to get user's choice of countries
        '''       
        self._curr.execute('SELECT name FROM Continents ORDER BY name')
        wholeworld = ['Worldwide']
        continents = list(zip(wholeworld, *self._curr.fetchall()))[0]
        
        prompt = 'What part of the world would you like to tour?'
        region = self._getChoice(prompt, continents)[0] 

        if region == -1 :   # User closed window without choosing
            return        
         
        cmd = self._getCommand(desired, region)   
        if region : 
            locale = continents[region]
            locale_str = f'in {locale}'
            self._curr.execute(cmd, (locale,))
        else :
            locale = ''
            locale_str = wholeworld[0]
            self._curr.execute(cmd)
            
        data = list(zip(*self._curr.fetchall()))[0]
        
        desired_str = desired if desired == 'area' else 'population'
        mini = MainWindow.MIN_COUNTRIES
        maxi = MainWindow.MAX_COUNTRIES
        
        if desired != 'general' :
            mini = MainWindow.MIN_COUNTRIES
            maxi = MainWindow.MAX_COUNTRIES
            self._handleAreaOrPop(data, locale, locale_str, desired, desired_str, mini, maxi)
        else :
            mini = 1
            maxi = MainWindow.MIN_COUNTRIES
            self._handleGeneral(data, locale, locale_str, desired, desired_str, mini, maxi)
    
            
    def _handleAreaOrPop(self, data, locale, locale_str, desired, desired_str, mini, maxi) :
        '''Get list of countries with population or area data'''
        cont_data = [self._curr.execute(f'''SELECT {desired} from Countries 
                WHERE name = ?''', (country,)).fetchone()[0] for country in data]
        cont_array = np.array(cont_data)
        prompt = f'Select between {mini} and {maxi} countries {locale_str} (sorted by {desired_str})'
        labelVar = f'Total Countries : {len(cont_array)}    Total {desired_str} : {np.sum(cont_array) : ,} '
        if desired == 'area' :
            labelVar += ' km\u00B2'
        choices = self._getChoice(prompt, data, labelVar, mini, maxi, multi = True)
        if choices[0] == -1 :  # user closed without choosing
            return
        self._launchCountries(desired, data, choices)


    def _handleGeneral(self, data, locale, locale_str, desired, desired_str, mini, maxi) :
        '''Get list of countries with general info'''
        prompt = f'Select between {mini} and {maxi} countries {locale_str} (sorted alphabetically)'
        labelVar = ''
        choices = self._getChoice(prompt, data, labelVar, mini, maxi, multi = True)
        if choices[0] == -1 : # user closed without choosing
            return
        self._launchCard(data, choices)
        

    def _getCommand (self, desired, region) :
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


    def _getChoice(self, prompt, continents, labelVar = '', mini = 1, maxi = 1, multi = False) :
        '''Get user's choice of which continent or countries to see'''
        dwin = DialogWindow(self, prompt, continents, mini, maxi, labelVar, multi)
        self.wait_window(dwin)
        choice = dwin.chosen
        return choice


    def _launchCountries(self, desired, countries, choices) :
        '''Display chosen countries by area or population'''
        # store countries and data in list to be used for bar chart
        barCountries = []
        barData = []
        # goes through the indices of the curselection of the countries
        for choice in choices :
            barCountries.append(countries[choice])
            self._curr.execute(f'''SELECT {desired} FROM Countries 
                                    WHERE name = ?''', (countries[choice],))
            data = self._curr.fetchone()[0]

            barData.append(data)
        countriesData = dict(zip(barCountries, barData))
        # call plotWindow to create barchart and boxplot
        PlotWindow(self, desired, choices, countriesData, bar = True)
        PlotWindow(self, desired, choices, countriesData)


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
        if tkmb.askokcancel('Confirm close', \
                        'Close all windows and quit?', parent = self) :
            self._conn.close()
            self.destroy()
            self.quit()


if __name__ == '__main__' :
    MainWindow().mainloop()
