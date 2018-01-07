import datetime

def average(data):
    return sum(data) / len(data)

def variance(data):
    avg = average(data)
    variance = 0
    for d in data:
        variance = variance + (avg - d) ** 2
    return variance / len(data)

def std_dev(data):
    return variance(data) ** 0.5

def date_range(date1, date2):
    for n in xrange((date2 - date1).days + 1):
        yield date1 + datetime.timedelta(n)
