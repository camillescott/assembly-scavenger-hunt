#! /usr/bin/python

import sys
import dnatextutils as utils

infile = sys.argv[1]
with open(infile, 'rb') as infp:
    for line in infp:
        if line[0] != '>':
            print utils.bin_to_text(utils.dna_to_bin(line))
