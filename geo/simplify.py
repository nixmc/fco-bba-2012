#!/usr/bin/env python

"""
Simplifies Polygon shapes in KML files, using the Douglas-Peucker line
simplification algorithm.

Writes simplified KML to STDOUT.
"""

import sys

import simplekml

from BeautifulSoup import BeautifulStoneSoup

from dp import simplify_points


def simplify(filename, basic=False):

    with open(filename) as fp:

        soup = BeautifulStoneSoup(fp)

        kml = simplekml.Kml()
        multipnt = kml.newmultigeometry(name="MultiPoint")

        # import pdb; pdb.set_trace()

        allcoords = sorted([coords.text.split() for coords in soup.findAll("coordinates")], key=lambda elem: len(elem), reverse=True)

        if basic and len(allcoords) > 1:
            allcoords = allcoords[:2]

        for coords_group in allcoords:
            coords = [map(float, line.split(",")) for line in coords_group]
            multipnt.newpolygon(name="",
                                outerboundaryis=simplify_points(coords, 0.01))

        return kml.kml()


if __name__ == "__main__":
    sys.stdout.write(simplify(sys.argv[1], basic=True))
