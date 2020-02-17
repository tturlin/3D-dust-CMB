#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-

## @package HEALPix
# This package provide class to manipulate HEALPix sky map.

import healpy as hp
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

__name__ = "healpix"

logger = logging.getLogger(__name__)

## This class provide utilities to manipulate full-sky map.
class HealpixMap():

    ## Constructor for the HealpixMap object.
    # @param self A pointer to the HealpixMap object.
    # @param path A Path object to the fits map you want to load.
    # @param field A string that contain the field of data you want to load.
    def __init__(self, path, field=None):
        self.path = path
        data_list, header = hp.read_map(self.path, field=field, h=True, hdu=1, memmap=True, verbose=False)
        j = 0
        self.data = []
        self.data_type = []
        for i in range(len(header)):
            if 'TTYPE' in header[i][0] and (header[i][1] not in ["HPXINDEX"]):
                self.data_type.append(header[i][1])
                self.data.append(data_list[j])
                j += 1
        self.__NSIDE = hp.get_nside(self.data[0])
        self.__NPIX = hp.nside2npix(self.__NSIDE)
        self.__PIX_SIZE = hp.nside2resol(self.__NSIDE, arcmin=True) / 60
        self.name = self.path.stem
        self.regions = []
        logger.info("HealpixMap created")
        logger.info("Pixel size: {}".format(self.__PIX_SIZE))

    ## Getter for the NSIDE parameter of the Healpix map.
    # @param self A pointer to the HealpixMap object.
    # @return The NSIDE parameter of the Healpix map.
    def get_nside(self):
        return self.__NSIDE

    ## Getter for the NPIX parameter of the Healpix map.
    # @param self A pointer to the HealpixMap object.
    # @return The NPIX parameter of the Healpix map.
    def get_npix(self):
        return self.__NPIX

    ## Getter for the PIX_SIZE parameter of the Healpix map.
    # @param self A pointer to the HealpixMap object.
    # @return The PIX_SIZE parameter of the Healpix map.
    def get_pix_size(self):
        return self.__PIX_SIZE

    ## Getter for the map name
    # @param self A pointer to the HEALPix object
    # @return The name of the HEALPix map
    def get_name(self):
        return self.name

    ## Draw a mollview projection of the data.
    # @param self A pointer to the HealpixMap object.
    # @param fig The figure number.
    # @param norm A string that allow to choose beetween "hist" for an histogram equalized map, "log" for a log color map or None for a linear color map.
    def draw_map(self, fig, norm=None):
        print("Data type are:")
        for i, key in enumerate(self.data_type):
            print("{}: {}".format(i, key))
        dtype = int(input("Which data do you want to show? "))

        hp.mollview(self.data[dtype], coord='G', title=self.data_type[dtype], norm=norm, fig=fig, xsize=4086)
        hp.graticule()
        logger.info("Sky map created, field loaded: {}".format(self.data_type[dtype]))

    ## Draw a square on the Healpix map.
    # @param self A pointer to the HealpixMap object.
    # @param lon The longitude of the center of the square, in degree.
    # @param lat The latitude of the center of the square, in degree.
    # @param lon_size The length of the square on the logitude axis, in degree.
    # @param lat_size The lenght of the square on the latitude axis, in degree.
    def draw_region(self, lon, lat, lon_size, lat_size):
        hp.projplot([lon - lon_size/2, lon + lon_size/2], 2 * [lat - lat_size/2], 'r+', lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot(2 * [lon + lon_size/2], [lat - lat_size/2, lat + lat_size/2], 'r+', lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot([lon - lon_size/2, lon + lon_size/2], 2 * [lat + lat_size/2], 'r+', lonlat=True) # FIXME Only draw the starting and ending point
        hp.projplot(2 * [lon - lon_size/2], [lat - lat_size/2, lat + lat_size/2], 'r+', lonlat=True) # FIXME Only draw the starting and ending point



    ## Show the map and any possible region on a matplotlib figure.
    # @param self A pointer to the HealpixMap object.
    # @param blocking Whether the plot is blocant or not.
    def show_map(self, blocking=False):
        plt.show(block=blocking)

    ## Create a HealpixRegion object that correspond to a part of the Healpix sky map
    # @param self A pointer to the HealpixMap object.
    # @param lon The longitude of the center of the HealpixRegion, in degree.
    # @param lat The latitude of the center of the HealpixRegion, in degree.
    # @param lon_size The size of the HealpixRegion along the longitude axis in degree.
    # @param lat_size The size of the HealpixRegion along the latitude axis in degree.
    # @param resol The size of a pixel in arcmin, which correspond to the resolution.
    # @return The HealpixRegion object.
    def create_region(self, lon, lat, lon_size, lat_size, resol=1.5):
        rdata = []
        res_deg = resol / 60
        lon_size = int(lon_size / res_deg)
        lat_size = int(lat_size / res_deg)
        for i in range(len(self.data)):
            rdata.append(hp.gnomview(self.data[i], rot=[lon, lat], xsize=lon_size, ysize=lat_size, coord='G', return_projected_map=True, reso=resol))
            plt.close()
        self.regions.append(HealpixRegion(lon, lat, lon_size, lat_size, rdata, self.data_type, res_deg, self))
        return self.regions[-1]

## This class provide utilities to manage sky region.
class Region():

    ## Constructor for the Region object.
    # @param self A pointer to the Region object.
    # @param lon The longitude of the center of the region, in degree.
    # @param lat The latitude of the center of the region, in degree.
    # @param lon_size The size of the region along the longitude axis, in degree.
    # @param lat_size The size of the region along the latitude axis, in degree.
    # @param data The data on this region.
    # @param data_type The type of the data on this region.
    # @param resol The resolution, which correspond to the pixel size, in degree.
    def __init__(self, lon, lat, lon_size, lat_size, data, data_type, resol):
        self.__LAT = lat
        self.__LON = lon
        self.__LAT_SIZE = lat_size
        self.__LON_SIZE = lon_size
        self.data = data
        self.data_type = data_type
        self.resolution = resol
        logger.info("Region created")
        logger.debug("Data shape: ({}, {})".format(len(self.data), self.data[0].shape))

    ## Getter for the latitude of the region, in degree.
    # @param self A pointer to the Region object.
    def get_lat(self):
        return self.__LAT

    ## Getter for the longitude of the region, in degree.
    # @param self A pointer to the Region object.
    def get_lon(self):
        return self.__LON

    ## Getter for the region's size along the latitude axis, in degree.
    # @param self A pointer to the Region object.
    def get_lat_size(self):
        return self.__LAT_SIZE

    ## Getter for the region's size along the longitude axis, in degree.
    # @param self A pointer to the Region object.
    def get_lon_size(self):
        return self.__LON_SIZE

    ## Draw the region of the sky.
    # @param self A pointer to the Region object.
    # @param fig The figure number.
    def draw_region(self, fig):
        print("Data type are:")
        for i, key in enumerate(self.data_type):
            print("{}: {}".format(i, key))
        dtype = int(input("Which data do you want to show? "))

        plt.figure(fig)
        X = np.linspace(self.__LON - self.__LON_SIZE/2, self.__LON + self.__LON_SIZE/2, np.shape(self.data[dtype])[0])
        Y = np.linspace(self.__LAT - self.__LAT_SIZE/2, self.__LAT + self.__LAT_SIZE/2, np.shape(self.data[dtype])[1])
        logger.debug("X shape: {}, x data shape: {}, Y shape: {}, y data shape: {}". format(np.shape(X), np.shape(self.data[dtype])[0], np.shape(Y), np.shape(self.data[dtype])[1]))
        XX, YY = np.meshgrid(Y, X)
        logger.debug("XX shape: {}, YY shape: {}, data shape: {}". format(XX.shape, YY.shape, self.data[dtype].shape))
        plt.pcolormesh(XX, YY, self.data[dtype], cmap="jet")
        plt.xlabel("Longitute")
        plt.ylabel("Latitude")
        plt.title(self.data_type[dtype])
        plt.colorbar()

    ## Show the region of the sky on a matplotlib figure.
    # @param self A pointer to the Region object.
    # @param blocking Wether the plot is blocant or not.
    def show_region(self, blocking=False):
        plt.show(block=blocking)

## This class provide utilities to manage sky region coming from HealpixMap.
class HealpixRegion(Region):

    ## Constructor for the HealpixRegion object.
    # @param self A pointer to the Region object.
    # @param lat The latitude of the center of the region, in degree.
    # @param lon The longitude of the center of the region, in degree.
    # @param lat_size The size of the region along the latitude axis, in degree.
    # @param lon_size The size of the region along the longitude axis, in degree.
    # @param data The data on this region.
    # @param data_type The type of the data on this region.
    # @param resol The resolution, which correspond to the pixel size, in degree.
    # @param Hpx The HealpixMap object corresponding to the full-sky map of this Region
    def __init__(self, lat, lon, lat_size, lon_size, data, data_type, resol, Hpx):
        super().__init__(lat, lon, lat_size, lon_size, data, data_type, resol)
        self.Hpx = Hpx
        logger.info("HealpixRegion created")
