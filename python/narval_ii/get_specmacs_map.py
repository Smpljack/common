# -*- coding: utf-8 -*-
import maptools

def _main():
    import sys
    if len(sys.argv) != 8:
        print("""USAGE:
{} <MAP ID> <NORTH> <WEST> <SOUTH> <EAST> <MIN PIXELS> <OUTFILE>
""".format(sys.argv[0]))
        return -1
    map_id = sys.argv[1]
    north, west, south, east = map(float, sys.argv[2:6])
    min_pixels = int(sys.argv[6])
    outfile = sys.argv[7]
    img = maptools.get_specmacs_map(map_id, north, west, south, east, min_pixels)
    img.save(outfile)
    return 0

if __name__ == '__main__':
    exit(_main())
