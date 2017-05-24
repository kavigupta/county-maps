"""
Runs the vote density
"""
from sys import argv
import os

from vote_density import create_vote_density_map

if not os.path.exists("outputs"):
    os.makedirs("outputs")

for cutoff_perc in 1, 50, 90, 95, 99, 99.5, 99.9, 100:
    create_vote_density_map("2016-results.csv", cutoff_perc, "outputs/colorized-election-%03.2f.svg" % cutoff_perc)
