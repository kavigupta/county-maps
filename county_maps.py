"""
A module containing utilities regarding county maps.
"""

import csv
import re

AREA_FILE = "areas.csv"
COUNTY_SHAPE = '(?P<pre>.*<path.*fill:#)(?P<color>[0-9a-fA-F]*)(?P<mid>;.*inkscape:label=")(?P<name>[^"]*)(?P<end>".*)'
IGNORE_STATES = ("AK", "DC")
UNFILLED_COUNTY_PATH = "counties.svg"

def _read_areas():
    areas = {}
    with open(AREA_FILE) as area_file:
        for county_name, _, _, area, *_ in csv.reader(area_file):
            if "," not in county_name:
                continue
            assert county_name not in areas, county_name
            areas[county_name] = float(area)
    areas.update({
        "Yakutat, AK" : 9463,
        "Wrangell, AK" : 3462,
        "Denali, AK" : 12777,
        "Skagway, AK" : 464,
        "Broomfield, CO" : 34,
        "Fairfax Co., VA" : 406,
        "Oglala, SD" : 2097
    })
    return areas

class Area:
    """
    An interface for getting the area in square miles of a county.
    """
    areas = _read_areas()
    @classmethod
    def of_county(cls, county):
        """
        Get the area for the given county
        """
        return cls.areas[county]

counties = set(Area.areas)

with open(UNFILLED_COUNTY_PATH) as _unfilled_county:
    UNFILLED_COUNTY_SVG = _unfilled_county.read()

def color_map(county_colors, original_map=UNFILLED_COUNTY_SVG, ignore_states=IGNORE_STATES):
    """
    Colors the given original_map string and returns the result as a string.
        county_colors: map from county names [as in `counties`] to hex colors
        original_map: the text of an svg file of an unfilled county map (UNFILLED_COUNTY_SVG by default)
        ignore_states: states to color with the default background color (DC and Alaska by default)
    """
    mapping = {}
    for county, color in county_colors.items():
        if county.replace(",", " city,") in counties:
            mapping[county.replace(",", " County,")] = color
    for county, color in county_colors.items():
        mapping[county.replace(" city", "")] = color
    def _gen():
        for line in original_map.split("\n"):
            match = re.match(COUNTY_SHAPE, line)
            if not match:
                yield line
                continue
            name = match.group("name")
            if name[-2:] in ignore_states:
                hexa = "252525"
            else:
                hexa = "{0:06x}".format(mapping[name])
            pre, _, *rest = list(match.groups())
            yield "".join([pre, hexa] + rest)
    return "\n".join(_gen())
