'''
Countries Data Code Driver
Authors: Surajit Bose, James Kang
Copyright © 2023

This project relies on the REST Countries API by Alejandro Matos: 
    - https://restcountries.com/
    - https://gitlab.com/restcountries/restcountries

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at https://mozilla.org/MPL/2.0/
'''

import backend
import frontend

if __name__ == '__main__' :
    backend.main()
    frontend.MainWindow().mainloop()