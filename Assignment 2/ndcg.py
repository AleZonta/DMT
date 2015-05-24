#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import sys

# [(float, float)] (confidence, score)
def nDCG(rows):
    max_score = 0.0
    score = 0.0
    for i, elem in enumerate(sorted(rows, key=lambda x: float(x[0]), reverse=True)):
        score += float(elem[1]) / (i + 1)
    for i, elem in enumerate(sorted(rows, key=lambda x: float(x[1]), reverse=True)):
        max_score += float(elem[1]) / (i + 1)
    if max_score:
        return score / max_score
    else:
        return 1

def process_rows(rows):
    last = None
    search_entries = [] # entries with the same search_id
    results = []
    for row in rows:
        #assert len(row) == 3
        if len(row) != 3:
            import ipdb; ipdb.set_trace()
        curr = int(row[0])
        if last != curr:
            if len(search_entries) > 0:
                results.append(nDCG(search_entries))
            search_entries = []
            last = curr
        search_entries.append(row[1:])
    if len(search_entries) > 0:
        results.append(nDCG(search_entries))
    return sum(results) / len(results)


# the input file should have 3 columns - search_id, confidence, score (0, 1, 5)
def process_file(infile_path):
    with open(infile_path) as infile:
        reader = csv.reader(infile)
        return process_rows(reader)

if __name__ == '__main__':
    #import ipdb; ipdb.set_trace()
    print process_file(sys.argv[1])
