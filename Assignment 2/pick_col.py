#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import collections
import csv
import sys

def pick_col(filename, col):
    with open(filename) as f:
        reader = csv.reader(f)
        colnum = None
        first_line = True
        for line in reader:
            if first_line:
                first_line = False
                try:
                    colnum = int(col)
                except:
                    for i, item in enumerate(line):
                        if item == col:
                            colnum = i
                    if colnum is None:
                        raise RuntimeError('Column not found')
            else:
                yield line[colnum]


if __name__ == '__main__':
    rows = pick_col(sys.argv[1], sys.argv[2])

    # all
    #print '\n'.join(rows)

    # nulls
    #all = 0.0
    #non_null = 0.0
    #for x in rows:
        #all += 1
        #if x != 'NULL':
            #non_null += 1
    #print non_null / all * 100

    # all unique counted
    counts = collections.defaultdict(lambda: 0)
    for row in rows:
        counts[row] += 1
    # sort by number of results
    print '\n'.join('%s:%d' % (k, v) for k, v in sorted(counts.iteritems(), key=lambda x: x[1], reverse=True))
    print len(counts)
