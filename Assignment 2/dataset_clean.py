#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2015 Andrei Tatar. All rights reserved.

import sys
import csv


def rm_col(num, lines):
    for line in lines:
        del line[num]
        yield line

def compact_comp(lines):
    for line in lines:
        rank = 0
        comps = 8
        for i in xrange(8):
            if line[26 + i*3] == 'NULL' or line[26 + i*3 + 1] in ('NULL', '-1'):
                comps -= 1
            else:
                rank += int(line[27 + i*3])
        if comps:
            line[26:50] = ['%5.3f' % (float(rank)/comps)]
        else:
            line[26:50] = ['NULL']
        yield line

def compact_clickbooking(lines):
    for line in lines:
        clickscore = int(line[-3]) + 5 * int(line[-1])
        del line[-3]
        line[-1] = str(clickscore)
        yield line

infile = csv.reader(open(sys.argv[1]))
try:
    outfile = csv.writer(open(sys.argv[2], 'w'))
except IndexError:
    outfile = csv.writer(open('compressed.csv', 'w'))

head = infile.next()
new_head = head[:]

if 'position' in head:
    del new_head[14]
    del new_head[-3]
    new_head[-1] = 'click_score'
    new_rows = compact_clickbooking(compact_comp(rm_col(14, infile)))
else:
    new_rows = compact_comp(infile)

new_head[26:50] = ['comp_rank']
outfile.writerow(new_head)
outfile.writerows(new_rows)

