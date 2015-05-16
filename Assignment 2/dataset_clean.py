#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import csv

POSITION_COL = 14
BOOK_COL = -1
CLICK_COL = -3
COMP_START_COL = 26
COMP_END_COL = 50


def rm_col(num, lines):
    for line in lines:
        del line[num]
        yield line

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
    new_rows = compact_clickbooking(compact_comp(rm_col(POSITION_COL, infile)))
else:
    new_rows = compact_comp(infile)

new_head[COMP_START_COL:COMP_END_COL] = ['comp_rank']
outfile.writerow(new_head)
outfile.writerows(new_rows)

