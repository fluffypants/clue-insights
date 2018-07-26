import datetime

def average(data):
    return sum(data) / float(len(data))

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

def weekday_from_int(n):
    return {
      0: "Mon",
      1: "Tue",
      2: "Wed",
      3: "Thu",
      4: "Fri",
      5: "Sat",
      6: "Sun"
    }[n]
