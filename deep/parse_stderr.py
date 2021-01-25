#! /usr/bin/python

import os, sys
import re
import datetime
import numpy as np
from scipy import stats
import json
import copy

options = {
    "skip" : 1000
}

date_format  = '%d-%b-%Y %H:%M:%S.%f'
date_format_tz  = '%Y-%m-%d %H:%M:%S'

def parse(
        logs, 
        skip = 10
        ):
    line_pattern = re.compile(r'Begin processing the (\d+)(st|nd|rd|th) record. Run (\d+), Event (\d+), LumiSection (\d+) on stream (\d+) at (\d\d-...-\d\d\d\d \d\d:\d\d:\d\d.\d\d\d) .*')

    events = []
    times = []
    nvalues = 0
    with open(logs, "r") as f:
        lines = f.readlines()
        for l in lines:
            line = l.rstrip("\n")
            matches = line_pattern.match(line)
            if matches:
                event = int(matches.group(1))
                time = datetime.datetime.strptime(matches.group(7) + "000", date_format)
                if event <= skip:
                    nvalues += 1
                    continue
                events.append(event)
                times.append(time)

    return (events[0:-nvalues], times[0:-nvalues])

def parseNetLog(pathToNet):
    with open(pathToNet, "r") as f:
        lines = f.readlines()
        lbytes = []
        lts = []
        for line in lines:
            values = line.split(" ")
            bytess = int(values[-1])
            ts = " ".join(values[:-1]).split("-")[:-1]
            ts = "-".join(ts)
            ts = datetime.datetime.strptime(ts, date_format_tz)
            lbytes.append(bytess)
            lts.append(ts)
        return lts, lbytes

class SomeFit:
    def __init__(self):
        self.slope = 0

def analyze_one_task(pathToStderr, referenceTime=datetime.datetime(2020, 1, 1)):
    # parse stuff
    events, times = parse(pathToStderr, **options)

    # output will be in the same folder
    justPath = pathToStderr.split("/")[0:-1]
    #outName = os.path.join("/".join(justPath), "logs.json")

    # fit and obtain throughput values
    try:
        fit = stats.linregress(np.array([(t - referenceTime).total_seconds() for t in times]), np.array(events))
    except:
        print("failed to parse task %s" % pathToStderr)
        fit = SomeFit()
        #raise ValueError("failed ot parse task % " % pathToStderr)

    outputData = {
        "throughput": fit.slope,
        "referenceTime" : referenceTime.strftime(date_format),
        "skip" : options["skip"],
        "events" : events,
        #"times" : [t.strftime(date_format) for t in times]
        "times" : times
    }

    #jsonOutputData = copy.deepcopy(outputData)
    #jsonOutputData["times"] = [t.strftime(date_format) for t in times]
    #with open(outName, "w") as f:
    #    f.write(json.dumps(jsonOutputData, indent=4))

    return outputData

def main():
    pathToStderr = sys.argv[1]
    referenceTime = datetime.datetime(2020, 1, 1)
    res = analyze_one_task(pathToStderr, referenceTime)
    print(res["throughput"])

if __name__ == "__main__":
    main()
