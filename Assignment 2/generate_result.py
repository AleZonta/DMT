#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import csv

SEARCH_ID_COL = 0
PROP_ID_COL = 7

def combine_results(tests, confidences, clickcol, bookcol):
    current_search = None
    search_results = []
    for test in tests:
        if test[SEARCH_ID_COL] != current_search:
            search_results.sort(key=lambda result: result[1] + 6*result[2], reverse=True)
            for result in search_results:
                yield (current_search, result[0])
            search_results = []
            current_search = test[SEARCH_ID_COL]
        confs = confidences.next()
        try:
            # In case the classifier gets confused and outputs a missing value... happened to me
            search_results.append((test[PROP_ID_COL], float(confs[clickcol]), float(confs[bookcol])))
        except ValueError:
            search_results.append((test[PROP_ID_COL], 0.1, 0.02))
    search_results.sort(key=lambda result:result[1] + 6*result[2], reverse=True)
    for result in search_results:
        yield (current_search, result[0])


if len(sys.argv) < 3:
    print "Usage: ./generate_result.py <original_test_file> <confidence_file> [<output_file>]"
    exit(1)

testfile = csv.reader(open(sys.argv[1]))
conffile = csv.reader(open(sys.argv[2]))
try:
    outfile = csv.writer(open(sys.argv[3], 'w'))
except IndexError:
    outfile = csv.writer(open('result.csv', 'w'))

thead = testfile.next()
chead = conffile.next()

outfile.writerow(('search_id', 'property_id'))
outfile.writerows(combine_results(testfile, conffile,
                                  chead.index('confidence(1)'), chead.index('confidence(6)')))
