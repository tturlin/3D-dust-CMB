#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
# version: 1.0.0

import healpy as hp
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

import healpix

logging.basicConfig(filename="log", level=logging.DEBUG, filemode='w')

data_name = Path("./data")

while data_name.is_dir() == True:
    print("Actual location: {}".format(data_name))
    possibilities = []
    for child in data_name.iterdir():
        possibilities.append(child.parts[-1])

    possibilities.append('..')

    print("Moving choice are:")
    for i in range(len(possibilities)):
        print("{}: {}".format(i, possibilities[i]))

    choice = 'Something'
    try:
        choice = int(choice)
    except:
        pass

    while type(choice) != int:
        try:
            choice = int(choice)
        except:
            choice = input("Your mouvement choice ? ")

    if choice == len(possibilities)-1:
        data_name = data_name.parent
    else:
        data_name = data_name / possibilities[choice]
    print()

try:
    hpx_map = healpix.HEALPix(data_name)
    logging.info("Data loaded: {}".format(hpx_map.get_name()))
except FileNotFoundError:
    logging.error("The data you're trying to load are not located here: {}".format(data_name.name))
    sys.exit()
except OSError:
    logging.error("The data you're trying to load are not HEALPix sky map. Data name: {}".format(data_name.name))
    sys.exit()

hpx_map.draw_map('G', "hist")
hpx_map.show_map()