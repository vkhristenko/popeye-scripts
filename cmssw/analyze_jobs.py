import sys, glob

from parse_stderr import *

def analyze_one_job(pathToJob):
    nodes_instances = glob.glob(os.path.join(pathToJob, "*"))
    results = {}
    for task in nodes_instances:
        t = task.split("/")[-1]
        hostname = t.split("__")[0]
        taskid = int(t.split("__")[1])
        if hostname not in results:
            results[hostname] = { "tasks": {} }

        if taskid == 0:
            try:
                lts, lbytes = parseNetLog(os.path.join(task, "netlogs"))
            except:
                lbytes = []
                lts = []
            results[hostname]["netlogs"] = {
                "timestamps": lts,
                "bytes": lbytes
            }

        stderr = os.path.join(task, "logs.stderr")
        resultsPerTask = analyze_one_task(stderr)
        assert(taskid not in results[hostname]["tasks"])
        results[hostname]["tasks"][taskid] = resultsPerTask
    return results

def sum_over_job(resultsPerJob):
    summ = 0
    ntasks = 0
    for key, resultsPerHost in resultsPerJob.items():
        for key1, result in resultsPerHost["tasks"].items():
            summ += result["throughput"]
            ntasks +=1 
    return (summ, ntasks)

def filterNetLogs(resultsPerNode):
    task0FirstT = resultsPerNode["tasks"][0]["times"][0]
    task0EndT = resultsPerNode["tasks"][0]["times"][-1]
    netlogs = resultsPerNode["netlogs"]
    skip0 = 0
    skip1 = 0
    for i in range(len(netlogs["bytes"])):
        if netlogs["timestamps"][i] < task0FirstT:
            skip0 += 1
            continue
        if netlogs["timestamps"][i] > task0EndT:
            skip1 += 1
            continue
    return skip0, skip1

def main():
    pathToJobs = sys.argv[1]
    jobs = sys.argv[2:]
    results = {}
    for jj in jobs:
        j = glob.glob(os.path.join(pathToJobs, "*%s*" % jj))[0]
        resultsPerJob = analyze_one_job(j)
        assert(len(resultsPerJob.keys()) not in results)
        results[len(resultsPerJob.keys())] = resultsPerJob

    print("%10s %15s %10s" % ("nodes", "Average Evs/s", "Total Evs/s"))
    for nnodes, resultsPerJob in sorted(results.items(), key=lambda tup: tup[0]):
        (summ, ntasks) = sum_over_job(resultsPerJob)
        print("%10d %12.2f %10d" % (nnodes, summ/ntasks, summ))

if __name__ == "__main__":
    main()
