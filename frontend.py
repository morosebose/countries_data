'''
CIS 41B Spring 2023
Surajit A. Bose, James Kang
Final Project Front End
'''

# import modules
import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
import webbrowser
from os.path import exists
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class DisplayWindow(tk.Toplevel):
    ''' class to display individual cards -> gets called for every country selected'''
    def __init__(self, master, name, official, capital, pop, area, lang, currency, continent, url) :
        super().__init__(master)
        
        # i dont think we want these. i just copied and pasted from DialogWin
        # self.grab_set()
        # self.focus_set()
        self.transient(master)
        self.promptStr = tk.StringVar()
        self.promptStr.set(f"General Information {name}")

        # make frame & labels for country card
        F = tk.Frame(self)
        tk.Label(F, textvariable=self.promptStr, font=("Calibri", 13), padx=10,
                 pady=10).grid()
        tk.Label(F, text=name, font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text=official, font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Capital: " + str(capital), font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Population: " + str(pop), font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Area: " + str(area), font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Language: " + str(lang), font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Currency: " + str(currency), font=("Calibri", 13), fg="blue").grid()
        tk.Label(F, text="Continent: " + str(continent), font=("Calibri", 13), fg="blue").grid()
        F.grid(pady=20, padx=10)
        tk.Button(self, text="Visit on Google Maps", fg="blue", font=("Calibiri",8), command=lambda: webbrowser.open(url)).grid(padx=5, pady=10)


class PlotWindow(tk.Toplevel):

    ''' class to display boxplot & Bar Chart'''
    def __init__(self, master, filter, continent, data, bar = None):
        super().__init__(master)

        self.grab_set()
        self.focus_set()
        self.transient(master)

        # Need to put title still
        # self.promptStr = tk.StringVar()
        # self.promptStr.set(f"MAKE BOXPLOT OF THESE COUNTRIES: {data}")
        # tk.Label(self, textvariable=self.promptStr, font=("Calibri", 13), padx=10,
        #          pady=10).grid()

        fig = plt.figure(figsize=(10,10))
        if bar:
            country = []
            data_val = []
            for item in data.items():
                country.append(item[0]), data_val.append(item[1])
            print(country)
            print(type(country))
            print(data_val)
            print(type(data_val))
            plt.bar(country, data_val)
        else:
            # data is going to be a numpy array of either population or area of the selected continents/world-wide
            print(type(data))
            plt.title(f"Box Plot of {filter} for {continent}")
            #vert=0 goes horizontal
            plt.boxplot(data, vert=0)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class DialogWindow(tk.Toplevel):
    '''

    '''

    def __init__(self, master, prompt, data, multi=False):
        '''

        '''
        super().__init__(master)
        self.grab_set()
        self.focus_set()
        self.transient(master)
        self._choice = -1
        # variable to store the prompt for user to select all/continents or to select countries (up to 5)
        self.promptStr = tk.StringVar()
        self.promptStr.set(prompt)
        tk.Label(self, textvariable=self.promptStr, font=("Calibri", 13), padx=10,
                 pady=10).grid()

        frame = tk.Frame(self)
        self._sb = tk.Scrollbar(frame, orient='vertical')
        if multi:
            self._lb = tk.Listbox(frame, height=6, selectmode="multiple", yscrollcommand=self._sb.set)
        else:
            self._lb = tk.Listbox(frame, height=6, yscrollcommand=self._sb.set)
        self._sb.config(command=self._lb.yview)
        self._lb.grid(row=0, column=0)
        self._sb.grid(row=0, column=1, sticky='NS')
        frame.grid(row=1, column=0, padx=10, pady=10)
        self._lb.insert(tk.END, *data)
        tk.Button(self, text='Click to select', command=self._setChoice).grid(padx=5, pady=10)

        self.protocol("WM_DELETE_WIDOW", self._close)

    def _setChoice(self):
        self._choice = self._lb.curselection()
        print(self._choice)
        self.destroy()

    def getChoice(self):
        return self._choice
        # return self._choice

    # @property
    # def chosen(self):
    #     return self.choice

    def _close(self):
        self._choice = []
        self.destroy()


class MainWindow(tk.Tk):
    """

    """

    COUNTRIES_DB = 'countries.db'

    def __init__(self):
        """
        created the connection to the database.. ans the .cursor() to access database

        """
        super().__init__()

        self._conn = sqlite3.connect(MainWindow.COUNTRIES_DB)
        self._curr = self._conn.cursor()

        self.display_windows = []
        self.title("Tour De World")
        # places the window in the middle of the screen
        self.geometry("+500+500")
        # Main title of Application
        tk.Label(self, text="Tour de World", font=("Calibri", 15)).grid(pady=5)

        # Label to prompt & buttons to lock in choice
        tk.Label(self, text="Search Countries Data By  :", font=("Calibri", 13)).grid(pady=3)
        buttonFrame = tk.Frame(self)
        tk.Button(buttonFrame, text="Area", command=lambda: self.getContinentChoice('area')).grid(row=2, column=0)
        tk.Button(buttonFrame, text="Population", command=lambda: self.getContinentChoice('pop')).grid(row=2,
                                                                                                              column=1)
        tk.Button(buttonFrame, text="General Info", command=lambda: self.getContinentChoice('general')).grid(row=2,column=2)
        buttonFrame.grid(pady=3)

        self.protocol("WM_DELETE_WINDOW", self.mainWinClose)

    def getContinentChoice(self, filter):
        '''

        '''
        # PROMPT USER: For what part of the world?
        # get all continents from the Continents table
        self._curr.execute("SELECT name FROM Continents")
        # add, "world-wide" as one of the options
        wholeworld = ["World Wide"]
        continents = list(zip(wholeworld, *self._curr.fetchall()))[0]
        print(
            continents)  # ("World Wide - 'the whole shabang'", 'Asia', 'Oceania', 'Europe', 'North America', 'Antarctica', 'South America', 'Africa')
        # pass in variable prompt, to prompt user to choose the part of the world first..
        prompt = 'What part of the world would you like to tour?'
        choices = self._getChoice(prompt, continents) # <- self._getChoice() returns the choice of continent/whole-world in a tuple

        # i dont think i need this.
        if not choices:
            return
        
        choice = choices[0]

        # # REALLY HAVE TO CLEAN THIS BOTTOM PART UP, BUT IT WORKS FOR NOW.
        # # I'VE UNIT TESTED EVERY RUN, AND IT DOEST WORK.....,
        # # JUST GOTTA CLEAN IT UP AND PUT MAX NUMS FOR COUNTRIES
        
        # PROMPT USER: For which countries?
        # if filter is area or pop, display countries in ORDER BY area or pop
        if choice != 0 and (filter == "area" or filter == 'pop'):
            print(f"User chose {continents[choice]}!!!!")
            self._curr.execute(f"""SELECT Countries.name FROM Countries JOIN Continents 
                                    ON Countries.continent = Continents.id 
                                    WHERE Continents.name = ?
                                    ORDER BY Countries.{filter} DESC;""", (continents[choice],))  # ASC|DESC;
            countries = list(zip(*self._curr.fetchall()))[0]
            prompt = f'Select up to 5 countries: \n\n[Sorted by {filter} (Descending)]'
            print(countries)
            print(len(countries))
            # continent_data = []
            # for country in countries:
            #     self._curr.execute(f"""SELECT {filter} FROM Countries
            #                                             WHERE name = ?;""", (country,))
            #     data = self._curr.fetchone()[0]
            #     continent_data.append(data)

            # above, but using list comprehension
            continent_data = [self._curr.execute(f"""SELECT {filter} FROM Countries
                                                            WHERE name = ?;""", (country,)).fetchone()[0] for country in countries]
            print(continent_data)
            print(type(continent_data))
            continent_data = np.array(continent_data)
            print(type(continent_data))
            boxPlot = PlotWindow(self, filter, continents[choice], continent_data )

        # if filter is general, do not use ORDER BY to display countries, use SORTED by alphabetical order
        elif choice !=0 and filter =='general':
            print(f"User chose General & {continents[choice]}!!~~~~~")
            self._curr.execute(f"""SELECT Countries.name FROM Countries JOIN Continents 
                                    ON Countries.continent = Continents.id 
                                    WHERE Continents.name = ?""", (continents[choice],))
            country = list(zip(*self._curr.fetchall()))[0]
            # sorts the countries in alphabetical order
            countries = tuple(sorted(country))
            print(len(countries))
            # print('Sorted Tuple :', countries)
            # print(type(countries))
            prompt = f'Select up to 5 countries: '

        else:
            if (filter == "area" or filter == 'pop'):
                print("User chose World-Wide!!?!?!")
                self._curr.execute(f"""SELECT name FROM Countries
                                        ORDER BY {filter} DESC;""")
                countries = list(zip(*self._curr.fetchall()))[0]
                print(len(countries))
                prompt = f'Select up to 5 countries: \n\n[Sorted by {filter} (Descending)]'
                # continent_data = []
                # for country in countries:
                #     self._curr.execute(f"""SELECT {filter} FROM Countries
                #                             WHERE name = ?;""", (country, ))
                #     data = self._curr.fetchone()[0]
                #     continent_data.append(data)
                continent_data = [self._curr.execute(f"""SELECT {filter} FROM Countries
                                                                    WHERE name = ?;""", (country,)).fetchone()[0] for country in countries]
                print(continent_data)
                print(type(continent_data))
                continent_data = np.array(continent_data)
                print(type(continent_data))
                boxPlot = PlotWindow(self, filter, continents[choice], continent_data)
            else:
                print("User chose World-Wide!_!_!_!_!")
                self._curr.execute(f"""SELECT name FROM Countries""")
                countries = list(zip(*self._curr.fetchall()))[0]
                print(len(countries))
                prompt = f'Select up to 5 countries: \n\n[Sorted by {filter} (Descending)]'
                
        choices = self._getChoice(prompt, countries, multi=True)
        if filter == 'area' or filter == 'pop':
            self._launchCountries(filter, countries, choices)
        else:
            self._launchCard(countries, choices)

    def _getChoice(self, prompt, continents, multi=None):
        dwin = DialogWindow(self, prompt, continents, multi)
        self.wait_window(dwin)
        choice = dwin.getChoice()
        # print(choice)
        # print(type(choice))
        return choice
        # print(choice)

    def _launchCountries(self, filter, countries, choices):
        # store countries and data in list to be used for bar chart
        barCountries = []
        barData = []
        # goes through the indices of the curselection of the countries
        for choice in choices:
            barCountries.append(countries[choice])
            print(countries[choice])
            self._curr.execute(f"""SELECT {filter} FROM Countries 
                                    WHERE name = ?;""", (countries[choice],))
            data = self._curr.fetchone()[0]
            print(data)
            barData.append(data)
        print(barCountries)
        print(barData)
        countriesData = dict(zip(barCountries, barData))
        # call plotWindow to create barchart
        barChart = PlotWindow(self, filter, choices, countriesData, bar=True)

    def _launchCard(self, countries, choices):
        for choice in choices:
            name = countries[choice]
            # joins all tables, Countries, Continents, Languages, Capitals, Currencies with their C_C_JN <- i get it but idk how to write it?
            # like i'm using the _JN tables to do the many to many joining .. brain dead. 
            self._curr.execute("""SELECT C.name, C.official, CAP.name, C.pop, C.area,  L.name, CUR.name, CO.name, C.map 
                                    FROM Countries C, Continents CO
                                    INNER JOIN Count_Lang_Jn CL on C.id = CL.country
                                    INNER JOIN Languages L on CL.language = L.id
                                    INNER JOIN Count_Cap_Jn CC on C.id = CC.country
                                    INNER JOIN Capitals CAP on CC.capital = CAP.id
                                    INNER JOIN Count_Curr_Jn CR on C.id = CR.country
                                    INNER JOIN Currencies CUR on CR.currency = CUR.id
                                    WHERE C.continent = CO.id AND C.name = ?;""", (name, ))
            country_name, official, capital, pop, area, lang, currency, continent, url = self._curr.fetchone()
            print(country_name, official, capital, pop, area, lang, currency, continent, url)
            # WORKS YO! maybe we can add  the flag and use the flag on the card too

            DisplayWindow(self, country_name, official, capital, pop, area, lang, currency, continent, url)

    def mainWinClose(self):
        """
        callback function to quit the program and all memory when user clicks "X"
        """
        self.destroy()
        self.quit()

    def cur(self):
        return self._curr


if __name__ == '__main__':
    MainWindow().mainloop()
