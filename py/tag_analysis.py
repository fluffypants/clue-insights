import argparse
import datetime
from dateutil.parser import parse
import json
import sys
from util import average, std_dev, date_range

"""
A script for analysing a user-defined custom tag.
Optionally prints dates and presence of tag as csv.
"""

def load_tag_data(path, tag):
    data = None
    with open(path) as f:
        data = json.loads(f.read())
    days = []
    for i in data['data']:
        if tag in i['tags']:
            days.append(parse(i['day']))
    days.sort()
    return days

def analyse_deltas(path, tag, print_csv=False):
    data = load_tag_data(path, tag)
    if len(data) == 0:
        print "No tags found. Are you sure '%s' is the correct tag?" % tag
        return
    deltas = []
    for d in xrange(len(data)-1):
        delta = data[d+1] - data[d]
        if delta.days > 2:
            deltas.append(delta.days)
    if print_csv:
        print "CSV:"
        print "date,%s" % tag
        for d in date_range(data[0], data[len(data)-1]):
            if d in data:
                print str(d) + ",1"
            else:
                print str(d) + ",0"
        return
    print "==============="
    print "Average amount of days between %s: " % tag, average(deltas)
    print "Std dev: ", std_dev(deltas)
    print "Last day with %s: " % tag, data[len(data)-1]
    print "Days between today and last day with %s: " % tag, (datetime.datetime.today().date() - data[len(data)-1].date()).days
    print "==============="

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse tag data from the Clue app.')
    parser.add_argument('-p', '--path', help='path to Clue backup data file', required=True)
    parser.add_argument('-t', '--tag', help='tag to process', required=True)
    parser.add_argument('--csv', action='store_true', help='print as csv (date, has_tag)')
    args = parser.parse_args()
    analyse_deltas(args.path, args.tag, args.csv)
