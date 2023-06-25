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



class PlotWindow(tk.Toplevel):

    ''' class to display boxplot & Bar Chart'''
    def __init__(self, master, data, bar = None):
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
            # demo, gotta ge tour own data in
            np.random.seed(10)
            data = np.random.normal(100, 20, 200)
            plt.boxplot(data)

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
        if choices:
            choice = choices[0]
        else:
            return

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
            boxPlot = PlotWindow(self, countries )


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
                boxPlot = PlotWindow(self, countries)
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
        barChart = PlotWindow(self, countriesData, bar=True)


    def _launchCard(self, countries, choices):
        for choice in choices:
            name = countries[choice]
            self._curr.execute("""""")
        cards = DisplayWindow(self, countries, choices)





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
