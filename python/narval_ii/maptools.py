# -*- coding: utf-8 -*-
"""
Map generation tools for NARVAL-II
"""

import tilenames
import requests
import numpy as np
from PIL import Image

SPECMACS_TILE_URL = "https://macsserver.physik.uni-muenchen.de/campaigns/maps/NARVAL-II/{map_id}/{z}/{x}/{y}.png"

def get_specmacs_map(map_id, lat_north, lon_west, lat_south, lon_east, min_pixels):
    left, top = tilenames.latlon2relativeXY(lat_north, lon_west)
    right, bottom = tilenames.latlon2relativeXY(lat_south, lon_east)
    ref_len = max([bottom-top, right-left])
    zoom = int(np.ceil(np.log2(min_pixels / (256. * ref_len)))) 
    num_tiles = 2**zoom
    tiles_x = range(int(num_tiles*left), int(num_tiles*right)+1)
    tiles_y = range(int(num_tiles*top), int(num_tiles*bottom)+1)
    img = Image.new("RGBA", (256*len(tiles_x), 256*len(tiles_y)), (0, 0, 0, 0))
    for ix, x in enumerate(tiles_x):
        for iy, y in enumerate(tiles_y):
            res = requests.get(SPECMACS_TILE_URL.format(map_id=map_id, x=x, y=y, z=zoom), stream=True)
            if res.ok:
                tile = Image.open(res.raw)
                img.paste(tile, (ix*256, iy*256))
    roi = (int(256*(num_tiles*left-tiles_x[0])),
           int(256*(num_tiles*top-tiles_y[0])),
           int(256*(num_tiles*right-tiles_x[0])),
           int(256*(num_tiles*bottom-tiles_y[0])))
    return img.crop(roi)

