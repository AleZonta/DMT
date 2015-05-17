#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import collections
import sys
import csv

# srch_id, date_time, site_id, visitor_hist_starrating, visitor_hist_adr_usd
#TO_BE_REMOVED = (0, 1, 2, 4, 5)

#TO_BE_REMOVED = ('srch_id', 'date_time', 'site_id', 'visitor_hist_starrating', 'visitor_hist_adr_usd', 'prop_id')
TO_BE_REMOVED = ('srch_id', 'date_time', 'site_id', 'visitor_hist_starrating', 'visitor_hist_adr_usd', 'prop_id', 'prop_location_score1', 'prop_location_score2', 'prop_log_historical_price', 'srch_adults_count', 'srch_room_count', 'random_bool', 'price_usd', 'srch_query_affinity_score', 'orig_destination_distance')

# makes it a set
def transform_row(head, line):
    return collections.OrderedDict(zip(head, line))

def rm_cols(cols, line):
    for col_name in cols:
        del line[col_name]
    return line

def rm_these_cols(cols):
    def f(line):
        return rm_cols(cols, line)
    return f

def compact_comp(line):
    is_head = line['comp1_rate'] == 'comp1_rate'
    smaller = 0
    for i in xrange(1, 9):
        if line['comp%d_rate' % i] != 'NULL' and line['comp%d_inv' % i] in ('1', '+1'):
            smaller += 1
        del line['comp%d_rate' % i]
        del line['comp%d_inv' % i]
        del line['comp%d_rate_percent_diff' % i]
    line['comp_rate'] = str(smaller) if not is_head else 'comp_rate'
    return line


def compact_clickbooking(line):
    is_head = line['click_bool'] == 'click_bool'
    if not is_head:
        clickscore = int(line['click_bool']) + 5 * int(line['booking_bool'])
    else:
        clickscore = 'score'
    del line['click_bool']
    del line['booking_bool']
    del line['position']
    del line['gross_bookings_usd']
    line['score'] = clickscore
    return line

def transform_srch_children_count(line):
    if line['srch_children_count'] == 'srch_children_count':
        return line
    line['srch_children_count'] = int(int(line['srch_children_count']) > 0)
    return line

infile = csv.reader(open(sys.argv[1]))
try:
    outfile = csv.writer(open(sys.argv[2], 'w'))
except IndexError:
    outfile = csv.writer(open('compressed.csv', 'w'))

#import ipdb; ipdb.set_trace()
head = infile.next()
rows = (transform_row(head, x) for x in infile)

filters = [compact_comp, transform_srch_children_count, rm_these_cols(TO_BE_REMOVED)]
if 'position' in head:
    filters.append(compact_clickbooking)

def apply_filters(row):
    for fltr in filters:
        row = fltr(row)
    return row

new_head = apply_filters(transform_row(head, head)).values()
outfile.writerow(new_head)
outfile.writerows(apply_filters(row).values() for row in rows)
