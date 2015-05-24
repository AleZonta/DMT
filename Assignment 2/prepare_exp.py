#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import sys
import random

CONF_1 = 2
CONF_6 = 1

#~ OUTPUT_HEADER = ['search_id', 'confidence', 'score']

def prepare(predfile, truefile, outfile):
    predfile.next()
    truefile.next()
    #~ outfile.writerow(OUTPUT_HEADER)
    for predrow in predfile:
        score = truefile.next()[0]
        try:
            confidence = float(predrow[CONF_1]) + 6*float(predrow[CONF_6])
            #~ confidence = random.random()
        except ValueError:
            confidence = 0.42
        outfile.writerow(
            (predrow[0], confidence, score)
        )


if __name__ == '__main__':
    pred = csv.reader(open(sys.argv[1]))
    true = csv.reader(open(sys.argv[2]))
    out = csv.writer(open(sys.argv[3], 'w'))
    prepare(pred, true, out)
