#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-

## @package HEALPix
# This package provide class to manipulate HEALPix sky map.

import healpy as hp
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

## This class provide utilities to manipulate full-sky map.
class HEALPix():

    ## Constructor for the full-sky map
    # @param self A pointer to the HEALPix object
    # @param path A Path object to the fits map you want to load
    def __init__(self, path):
        self.path = path
        self.data = hp.read_map(path)
        self.NSIDE = hp.get_nside(self.data)
        self.NPIX = hp.nside2npix(self.NSIDE)
        self.PIX_SIZE = hp.nside2resol(self.NSIDE, arcmin=True) / 60
        self.name = self.path.stem
        logging.info("HEALPix object created")

    ## Getter for the map name
    # @param self A pointer to the HEALPix object
    # @return The name of the HEALPix map
    def get_name(self):
        return self.name

    ## Getter for the NSIDE parameter of the HEALPix map
    # @param self A pointer to the HEALPix object
    # @return The NSIDE parameter of the HEALPix map
    def get_nside(self):
        return self.NSIDE

    ## Getter for the NPIX parameter of the HEALPix map
    # @param self A pointer to the HEALPix object
    # @return The NPIX parameter of the HEALPix map
    def get_npix(self):
        return self.NPIX

    ## Getter for the PIX_SIZE parameter of the HEALPix map
    # @param self A pointer to the HEALPix object
    # @return The PIX_SIZE parameter of the HEALPix map
    def get_pix_size(self):
        return self.PIX_SIZE

    ## Draw a mollview projection of the data
    # @param self A pointer to the HEALPix object
    # @param coord A character that described the coordinates used in the map, which is 'G' for Galactic or 'E' for Ecliptic
    # @param norm A string that allow to choose beetween "hist" for an histogram equalized map, "log" for a log color map or None for a linear color map
    def draw_map(self, coord, norm=None):
        hp.mollview(self.data, coord=coord, title=self.name, norm=norm)

    ## Draw a square on the HEALPix map
    # @param self A pointer to the HEALPix object
    # @param lat The latitude of the center of the square
    # @param dlat The lenght of the square of each side of the center
    # @param lon The longitude of the center of the square
    # @param dlon The length of the square of each side of the center
    def draw_region(self, lat, dlat, lon, dlon):
        hp.projplot([lat-dlat, lat-dlat], [lon-dlon, lon+dlon], lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot([lat+dlat, lat+dlat], [lon-dlon, lon+dlon], lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot([lat-dlat, lat+dlat], [lon-dlon, lon-dlon], lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot([lat-dlat, lat+dlat], [lon+dlon, lon+dlon], lonlat=True) # FIXME Only draw the starting and ending point

    ## Show the map and any possible region
    # @param self A pointer to the HEALPix object
    def show_map(self):
        plt.show()