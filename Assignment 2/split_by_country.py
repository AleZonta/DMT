#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import collections
import sys
import csv


# makes it a set
def transform_row(head, line):
    return collections.OrderedDict(zip(head, line))



infile = csv.reader(open(sys.argv[1]))
outfile_prefix = sys.argv[2] # prepended to all outfile names
try:
    country_codes = sys.argv[3]
except IndexError:
    # all above 1000 records
    country_codes = '219,100,55,31,99,129,215,220,59,216,98,158,117,205,132,39,92,103,15,32,81,4,' + \
            '202,14,109,73,41,56,80,225,35,18,70,50,164,60,138,181,154,53,221,9,26,212,23,88,' + \
            '137,223,48,157,127,2,178,206,13,224,213,211,17,145,68,156,45,230,30,27,74,33,125,' + \
            '229,102,113,42,162,47,123,16,194,106,119,97,149,96,159,40,37,152,134,155,186,187,86,200'
country_codes = set(map(int, country_codes.split(',')))

head = infile.next()
rows = (transform_row(head, x) for x in infile)

# open files - country code or "other"
files = {}
for cc in country_codes:
    files[cc] = csv.writer(open('%s.%d.csv' % (outfile_prefix, cc), 'w'))
files['other'] = csv.writer(open('%s.0.csv' % outfile_prefix, 'w'))

# header to all
for f in files.itervalues():
    f.writerow(head)

for row in rows:
    cc = int(row['prop_country_id'])
    if cc in country_codes:
        files[cc].writerow(row.keys())
    else:
        files['other'].writerow(row.keys())
