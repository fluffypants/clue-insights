import argparse
import datetime
from dateutil.parser import parse
import json
import sys
from util import average, std_dev, date_range

"""
A script for analysing a tag (the user defined custom ones) or a label (e.g. 'period')
Optionally prints as csv for export
"""

def load_data(path, filter_fn):
    with open(path) as f:
        data_sorted = sorted(json.loads(f.read())['data'], key=lambda x: x['day'])

    data = { x['day'][:10]: x for x in data_sorted }
    days = []
    day_of_cycle_dict = {}
    day_of_cycle = 0
    start_date = parse(data_sorted[0]['day'])
    end_date = parse(data_sorted[len(data_sorted)-1]['day'])
    dates = [x.date().strftime('%Y-%m-%d') for x in date_range(start_date, end_date)]

    for d in dates:
        try:
            i = data[d]
        except:
            if day_of_cycle != 0:
                day_of_cycle += 1
            continue
        if 'period' in i:
            if (day_of_cycle > 15 or day_of_cycle == 0) and i['period'] != 'spotting':
                day_of_cycle = 1
        if filter_fn(i):
            days.append(parse(i['day']))
            if day_of_cycle != 0:
                if not day_of_cycle_dict.get(day_of_cycle):
                    day_of_cycle_dict[day_of_cycle] = 1
                else:
                    day_of_cycle_dict[day_of_cycle] += 1
        if day_of_cycle != 0:
            day_of_cycle += 1

    return { "days": days, "day_of_cycle": day_of_cycle_dict }

def analyse(path, filter_fn, field_name, print_csv=False):
    data = load_data(path, filter_fn)
    occurrences = data['days']
    day_of_cycle = data['day_of_cycle']
    day_of_cycle_total = sum([day_of_cycle[x] for x in day_of_cycle])

    if len(occurrences) == 0:
        print "No tags found. Are you sure '%s' is the correct tag?" % tag
        return

    deltas = []
    for d in xrange(len(occurrences)-1):
        delta = occurrences[d+1] - occurrences[d]
        if delta.days > 2:
            deltas.append(delta.days)

    if print_csv:
        print "CSV:"
        print "date,%s" % field_name
        for d in date_range(occurrences[0], occurrences[len(occurrences)-1]):
            if d in occurrences:
                print str(d) + ",1"
            else:
                print str(d) + ",0"
        return

    print "==============="
    print "Day of cycle distribution"
    previous = None
    for k in sorted(day_of_cycle.keys()):
        if previous:
            if k - previous > 1:
                print ".\n."
        previous = k
        print ("Day %s:" % k).ljust(10), str(day_of_cycle[k]).ljust(4), round(day_of_cycle[k] / float(day_of_cycle_total), 2)
    print "==============="
    print "Total amount of days with %s: " % field_name, len(occurrences)
    print "Average amount of days between %s: " % field_name, average(deltas)
    print "Std dev: ", std_dev(deltas)
    print "Last day with %s: " % field_name, occurrences[len(occurrences)-1]
    print "Days between today and last day with %s: " % field_name, (datetime.datetime.today().date() - occurrences[len(occurrences)-1].date()).days
    print "==============="

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse tag data from the Clue app.')
    parser.add_argument('-f', '--file', help='Clue backup data file location', required=True)
    parser.add_argument('-t', '--tag', help='custom tag to process')
    parser.add_argument('-l', '--label', help='label that is not a tag, e.g. period')
    parser.add_argument('--csv', action='store_true', help='print as csv (date, has_tag)')
    args = parser.parse_args()
    if args.tag:
        filter_fn = lambda x: args.tag in x['tags']
        field_name = args.tag
    else:
        filter_fn = lambda x: len(x[args.label]) > 0
        field_name = args.label
    analyse(args.file, filter_fn, field_name, args.csv)
