import sys, os

from analyze_jobs import analyze_one_job, sum_over_job, filterNetLogs
from parse_stderr import date_format

from scipy import stats
import datetime
import numpy as np

def main():
    pathToJob = sys.argv[1]

    # analyze this guy
    results = analyze_one_job(pathToJob)
    nnodes = len(results.keys())
    referenceTime=datetime.datetime(2020, 1, 1)

    # print simple stats
    (summ, ntasks) = sum_over_job(results)
    print("%10s %15s %10s" % ("nodes", "Average Evs/s", "Total Evs/s"))
    print("%10d %12.2f %10d" % (nnodes, summ/ntasks, summ))

    # print node, task, startTime endTime
    print("%10s %10s %20s %20s" % ("hostname", "task id", "startTime", "endTime"))
    for hostname, resultsPerNode in results.items():
        for taskid, resultsPerTask in resultsPerNode["tasks"].items():
            print("%10s %10d %20s %20s" % (hostname, taskid, 
                resultsPerTask["times"][0].strftime(date_format).split(" ")[1], 
                resultsPerTask["times"][-1].strftime(date_format).split(" ")[1]))

    # 
    for hostname, resultsPerNode in results.items():
        skipFirst, skipLast = filterNetLogs(resultsPerNode)
        lbytes = resultsPerNode["netlogs"]["bytes"][skipFirst:-skipLast]
        lts = resultsPerNode["netlogs"]["timestamps"][skipFirst:-skipLast]
        fit = stats.linregress(
            np.array([(t - referenceTime).total_seconds() for t in lts]), 
            np.array(lbytes))
        for ts, bytess in zip(lts, lbytes):
            print(ts, bytess / 1024)
        print("bytes/s = %f" % fit.slope)

if __name__ == "__main__":
    main()
