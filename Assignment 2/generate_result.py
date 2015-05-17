#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import csv
import optparse

SEARCH_ID_COL = 0
PROP_ID_COL = 7

def combine_results(tests, confidence_set, col_ids, weights):
    current_search = None
    search_results = []
    for test in tests:
        if test[SEARCH_ID_COL] != current_search:
            search_results.sort(key=lambda entry: entry[1], reverse=True)
            for entry in search_results:
                yield (current_search, entry[0])
            search_results = []
            current_search = test[SEARCH_ID_COL]

        entry_score = 0.0
        for index, confs in enumerate(it.next() for it in confidence_set):
            try:
                score = weights[index] * \
                        (float(confs[col_ids[index][0]]) + 6*float(confs[col_ids[index][1]]))
            except ValueError:
                score = weights[index] * 0.42
            entry_score += score

        search_results.append((test[PROP_ID_COL], entry_score))

    search_results.sort(key=lambda entry: entry[1], reverse=True)
    for entry in search_results:
        yield (current_search, entry[0])


parser = optparse.OptionParser(usage='Usage: %prog [options] CONFIDENCE1 [CONFIDENCE2 ...]')
parser.add_option('-t', '--test-dataset',
                  help='unmodified test dataset, required')
parser.add_option('-o', '--output', default='result.csv',
                  help='output file; defaults to result.csv')
parser.add_option('-w', '--weights',
                  help="specify weights for confidence CSVs, separated by commas (e.g. '-w 1,0.5,0.77' )")

options, args = parser.parse_args()

if options.test_dataset is None:
    print 'No test dataset specified'
    parser.print_help()
    exit(1)

if not args:
    print 'No confidence files specified'
    parser.print_help()
    exit(1)

if options.weights is not None:
    try:
        weights = [float(weight) for weight in options.weights.split(',')]
    except ValueError:
        print 'Invalid weights specified'
        raise
    if len(weights) != len(args):
        print 'Number of weights and of confidence files do not match'
        exit(1)
else:
    weights = [1.0] * len(args)

testfile = csv.reader(open(options.test_dataset))
outfile = csv.writer(open(options.output, 'w'))
confidence_set = [csv.reader(open(filename)) for filename in args]

thead = testfile.next()
cheads = (conffile.next() for conffile in confidence_set)
col_indexes = [(head.index('confidence(1)'), head.index('confidence(6)')) for head in cheads]

outfile.writerow(('search_id', 'property_id'))
outfile.writerows(combine_results(testfile, confidence_set, col_indexes, weights))
