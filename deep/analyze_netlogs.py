import sys, os

from parse_stderr import parseNetLog, date_format
import datetime

from scipy import stats
import numpy as np

import matplotlib.pyplot as plt

def main():
    pathToNetlog = sys.argv[1]

    lts, lbytes = parseNetLog(pathToNetlog)
   

    ltsnew = []; lbytesnew = []
    for ts, bytess in zip(lts, lbytes):
        if ts >= datetime.datetime.strptime("25-Jan-2021 05:02:35.000000", date_format) and ts <= datetime.datetime.strptime("25-Jan-2021 05:07:01.000000", date_format):
            ltsnew.append(ts)
            lbytesnew.append(bytess)
            ltsnew.append(ts)
            lbytesnew.append(bytess)
    lts = ltsnew
    lbytes = lbytesnew

    lbytes = [value / 1024 / 1024 for value in lbytes]
    
    for ts, bytess in zip(lts, lbytes):
        print(ts.strftime(date_format), bytess)

    referenceTime=datetime.datetime(2020, 1, 1)
    fit = stats.linregress(
        np.array([(t - referenceTime).total_seconds() for t in lts]),
        np.array(lbytes))
    print("MB/s = %f" % (fit.slope / 1024 / 1024))

    x = np.array(lts)
    y = np.array([a-lbytes[0] for a in lbytes])
    dy = np.array([lbytes[i] - lbytes[i-1] if i>0 else 0 for i in range(len(lbytes))])
    plt.figure(1)
    plt.plot(x, y, 'o', color='black')
    plt.xlabel("timestamp")
    plt.ylabel("Rx MB")
    plt.savefig("test_netlogs.png")
    plt.figure(2)
    plt.plot(x, dy, 'o', color="black")
    plt.xlabel("timestamp")
    plt.ylabel("Rx MB/s")
    plt.savefig("test_netlogs_deriv.png")

if __name__ == "__main__":
    main()
