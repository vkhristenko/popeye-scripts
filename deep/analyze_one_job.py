import sys, os

from analyze_jobs import analyze_one_job, sum_over_job, filterNetLogs
from parse_stderr import date_format

from scipy import stats
import datetime
import numpy as np

import matplotlib.pyplot as plt

def main():
    pathToJob = sys.argv[1]

    # analyze this guy
    results = analyze_one_job(pathToJob)
    nnodes = len(results.keys())
    referenceTime=datetime.datetime(2020, 1, 1)

    # print simple stats
    (summ, ntasks, nnodes) = sum_over_job(results)
    print("%10s %25s %25s %10s" % ("nodes", "Average Evs/s per task", "Average Evs/s per node", "Total Evs/s"))
    print("%10d %23.2f %23.2f %8.2f" % (nnodes, summ/ntasks, summ/nnodes, summ))

    # print node, task, startTime endTime
    print("%10s %10s %20s %20s %10s" % 
        ("hostname", "task id", "startTime", "endTime", "Evs/s"))
    for hostname, resultsPerNode in results.items():
        for taskid, resultsPerTask in resultsPerNode["tasks"].items():
            if resultsPerTask["throughput"] == 0:
                print("%10s %10d %20s %20s %8.2f" % (hostname, taskid,
                    "INVALID", "INVALID",
                    resultsPerTask["throughput"]))
            else:
                print("%10s %10d %20s %20s %8.2f" % (hostname, taskid, 
                    resultsPerTask["times"][0].strftime(date_format).split(" ")[1], 
                    resultsPerTask["times"][-1].strftime(date_format).split(" ")[1],
                    resultsPerTask["throughput"]))

    # 
    print("%10s %10s %20s %20s" % ("hostname", "MB/s", "startTime", "endTime"))
    total = 0
    for hostname, resultsPerNode in results.items():
        skipFirst, skipLast = filterNetLogs(resultsPerNode)
        lbytes = resultsPerNode["netlogs"]["bytes"][skipFirst:-skipLast]
        lts = resultsPerNode["netlogs"]["timestamps"][skipFirst:-skipLast]
        if len(lbytes)==0:
            continue
        fit = stats.linregress(
            np.array([(t - referenceTime).total_seconds() for t in lts]), 
            np.array(lbytes))
        print("%10s %8.2f %20s %20s" % 
            (hostname, fit.slope / 1024 / 1024, 
                lts[0].strftime(date_format).split(" ")[1],
                lts[-1].strftime(date_format).split(" ")[1]))
        total += fit.slope / 1024 / 1024
    print("Aggregated Bandwidth = %10s MB/s" % (total))

    #
    sssss = """
    for hostname, resultsPerNode in results.items():
        print(len(resultsPerNode["cpuutil"]["cpuutil"]),
            len(resultsPerNode["cpuutil"]["cpuutil"][0]))

        Y = np.array([i for i in range(len(resultsPerNode["cpuutil"]["cpuutil"]))])
        X = np.array([i for i in range(len(resultsPerNode["cpuutil"]["cpuutil"][0]))])
        Z = np.array(resultsPerNode["cpuutil"]["cpuutil"])
        plt.figure(1)
        plt.contour([X, Y], Z)
        plt.savefig("cpuutil.png")
    """


if __name__ == "__main__":
    main()
