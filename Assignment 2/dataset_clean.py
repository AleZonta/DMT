#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import csv

POSITION_COL = 14
BOOK_COL = -1
CLICK_COL = -3
COMP_START_COL = 26
COMP_END_COL = 50

# srch_id, date_time, site_id, visitor_hist_starrating, visitor_hist_adr_usd
TO_BE_REMOVED = (0, 1, 2, 4, 5)

def rm_cols(lines, *cols):
    for line in lines:
        yield [el for index, el in enumerate(line) if index not in cols]

def compact_comp(lines):
    for line in lines:
        smaller = 0
        for i in xrange(8):
            if line[COMP_START_COL + i*3] != 'NULL' and line[COMP_START_COL + i*3 + 1] == '1':
                smaller += 1
        line[COMP_START_COL:COMP_END_COL] = [str(smaller)]
        yield line

def compact_clickbooking(lines):
    for line in lines:
        clickscore = int(line[CLICK_COL]) + 5 * int(line[BOOK_COL])
        del line[CLICK_COL]
        line[BOOK_COL] = str(clickscore)
        yield line

infile = csv.reader(open(sys.argv[1]))
try:
    outfile = csv.writer(open(sys.argv[2], 'w'))
except IndexError:
    outfile = csv.writer(open('compressed.csv', 'w'))

head = infile.next()
new_head = head[:]

if 'position' in head:
    del new_head[POSITION_COL]
    del new_head[CLICK_COL]
    new_head[BOOK_COL] = 'click_score'
    new_rows = rm_cols(compact_clickbooking(compact_comp(rm_cols(infile, POSITION_COL))), *TO_BE_REMOVED)
else:
    new_rows = rm_cols(compact_comp(infile), *TO_BE_REMOVED)

new_head[COMP_START_COL:COMP_END_COL] = ['comp_rank']
new_head = [el for index, el in enumerate(new_head) if index not in TO_BE_REMOVED]
outfile.writerow(new_head)
outfile.writerows(new_rows)

