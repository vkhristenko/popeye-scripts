import sys, os

from parse_stderr import parseNetLog, date_format
import datetime

from scipy import stats
import numpy as np

def main():
    # parse 
    pathToNetlog = sys.argv[1]
    lts, lbytes = parseNetLog(pathToNetlog)
    for ts, bytess in zip(lts, lbytes):
        print(ts.strftime(date_format), bytess / 1024 / 1024)

    # fit to get slope
    referenceTime=datetime.datetime(2020, 1, 1)
    fit = stats.linregress(
        np.array([(t - lts[0]).total_seconds() for t in lts]),
        np.array(lbytes))
    print("MB/s = %f" % (fit.slope / 1024 / 1024))

    # plot
    

if __name__ == "__main__":
    main()
