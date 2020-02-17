#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
# version: 1.0.0

from astropy.io import fits
import healpy as hp
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

import healpix

__name__ = "main"

logging.basicConfig(filename="log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            choice = input("Your mouvement choice? ")

    if choice == len(possibilities)-1:
        data_name = data_name.parent
    else:
        data_name = data_name / possibilities[choice]
    print()


try:
    hpx_map = healpix.HealpixMap(data_name, field=None)
    logger.info("Data loaded: {}".format(hpx_map.get_name()))
except FileNotFoundError:
    logger.error("The data you're trying to load are not located here. Data location: {}".format(data_name.name))
    sys.exit()
except OSError:
    logger.error("The data you're trying to load are not HEALPix sky map. Data name: {}".format(data_name.name))
    sys.exit()
except IndexError:
    logger.error("The field of data you're trying to load doesn't exist. Field index: {}".format(field))
    logger.debug("No verification of field validity!!!")
    sys.exit()


hpx_map.draw_map(1, "hist")
hpx_map.draw_region(0, 0, 4, 6)
hpx_map.show_map()
test = hpx_map.create_region(0, 0, 4, 6)
test.draw_region(2)
test.show_region(True)

print("testing blocant plot")