"""
Methods for generating and handling densities given a set of votes
"""

import csv
import numpy as np

from county_maps import IGNORE_STATES, Area, color_map

def vote_density(results_file, ignore_states=IGNORE_STATES):
    """
    Get the democratic and republican votes per square mile for the given results.
        results_file: a file that contains data in the format
                ?, democratic votes, republican votes, *, state, county, *
    """
    with open(results_file) as results_handle:
        votes = {}
        for line in csv.reader(results_handle):
            label, votes_dem, votes_gop, *_, state, county, _ = line
            if state in ignore_states:
                continue
            if not label:
                continue
            county_id = county.replace(" County", "").replace(" Parish", "") + ", " + state
            area = Area.of_county(county_id)
            votes[county_id] = float(votes_dem) / area, float(votes_gop) / area
        return votes

def color_for_density(dem, gop, cutoff):
    """
    Get the color corresponding to the given densities dem and gop, normalized against the cutoff
    """
    blue = dem/cutoff
    red = gop/cutoff
    maximal = max(red, blue)
    if maximal > 1:
        blue = blue/maximal
        red = red/maximal
    red, blue = int(red * 0xFF), int(blue * 0xFF)
    return (red << 16) | blue

def vote_color_map(votes, cutoff_percentile):
    """
    Create a color mapping from the given list of densities and putting the upper cutoff bounds at the given percentile.
    """
    cutoff = np.percentile(list(votes.values()), cutoff_percentile)
    return {county : color_for_density(dem, gop, cutoff) for county, (dem, gop) in votes.items()}

def create_vote_density_map(vote_results_file, cutoff_percentile, output):
    with open(output, "w") as f:
        f.write(color_map(vote_color_map(vote_density(vote_results_file), cutoff_percentile)))
