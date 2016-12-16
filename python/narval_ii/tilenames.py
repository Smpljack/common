#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# Translates between lat/long and the slippy-map tile
# numbering scheme
# 
# http://wiki.openstreetmap.org/index.php/Slippy_map_tilenames
# 
# Written by Oliver White, 2007
# Modified to use numpy by Tobias Kölling, 2016
# This file is public-domain
#-------------------------------------------------------
import numpy as np

def numTiles(z):
    return(2**z)

def sec(x):
    return(1/np.cos(x))

def latlon2relativeXY(lat, lon):
    x = (lon + 180) / 360
    y = (1 - np.log(np.tan(np.deg2rad(lat)) + sec(np.deg2rad(lat))) / np.pi) / 2
    return(x, y)

def latlon2xy(lat, lon, z):
    n = numTiles(z)
    x, y = latlon2relativeXY(lat, lon)
    return(n*x, n*y)
  
def tileXY(lat, lon, z):
    x, y = latlon2xy(lat, lon, z)
    return(int(x), int(y))

def xy2latlon(x, y, z):
    n = numTiles(z)
    rel_y = y / n
    lat = mercatorToLat(np.pi * (1 - 2 * rel_y))
    lon = -180.0 + 360.0 * x / n
    return(lat, lon)

def latEdges(y, z):
    n = numTiles(z)
    unit = 1 / n
    relY1 = y * unit
    relY2 = relY1 + unit
    lat1 = mercatorToLat(np.pi * (1 - 2 * relY1))
    lat2 = mercatorToLat(np.pi * (1 - 2 * relY2))
    return(lat1, lat2)

def lonEdges(x, z):
    n = numTiles(z)
    unit = 360 / n
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)

def tileEdges(x, y, z):
    lat1, lat2 = latEdges(y, z)
    lon1, lon2 = lonEdges(x, z)
    return((lat2, lon1, lat1, lon2)) # S,W,N,E

def mercatorToLat(mercatorY):
    return(np.rad2deg(np.arctan(np.sinh(mercatorY))))

def tileSizePixels():
    return(256)

def tileLayerExt(layer):
    if(layer in ('oam')):
        return('jpg')
    return('png')

def tileLayerBase(layer):
    layers = { \
    "tah": "http://cassini.toolserver.org:8080/http://a.tile.openstreetmap.org/+http://toolserver.org/~cmarqu/hill/",
        #"tah": "http://tah.openstreetmap.org/Tiles/tile/",
    "oam": "http://oam1.hypercube.telascience.org/tiles/1.0.0/openaerialmap-900913/",
    "mapnik": "http://tile.openstreetmap.org/mapnik/"
    }
    return(layers[layer])

def tileURL(x, y, z, layer):
    return "%s%d/%d/%d.%s" % (tileLayerBase(layer), z, x, y, tileLayerExt(layer))
