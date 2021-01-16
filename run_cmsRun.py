#! /usr/bin/env python

import sys
import os
import copy
import tempfile

import FWCore.ParameterSet.Config as cms
import copy
import imp
import itertools
import math
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime
import numpy as np
from scipy import stats

# set the output encoding to UTF-8 for pipes and redirects
from set_output_encoding import *
set_output_encoding(encoding='utf-8', force=True)

optionsExtra = {
    "threads" : 8,
    "streams" : 8,
    "events" : 1500,
    "reportEveryNEvents" : 50
}
optionsCmsRun = {
    "saveLogs" : True
}

def parseCmsCfg(filename):
    # parse the given configuration file and return the `process` object it define
    # the import logic is taken from edmConfigDump
    try:
        handle = open(filename, 'r')
    except:
        print("Failed to open %s: %s" % (filename, sys.exc_info()[1]))
        sys.exit(1)

    # make the behaviour consistent with 'cmsRun file.py'
    sys.path.append(os.getcwd())
    try:
        pycfg = imp.load_source('pycfg', filename, handle)
        process = pycfg.process
    except:
        print("Failed to parse %s: %s" % (filename, sys.exc_info()[1]))
        sys.exit(1)

    handle.close()
    return process

def applyExtraSettings(
        process,
        threads = 1,
        streams = 1,
        events = 100,
        reportEveryNEvents = 100,
        inputFiles = []
        ):
    # set the number of streams and threads
    process.options.numberOfThreads = cms.untracked.uint32( threads )
    process.options.numberOfStreams = cms.untracked.uint32( streams )
  
    # set the number of events to process
    process.maxEvents.input = cms.untracked.int32( events )
  
    # print a message every 100 events
    if not 'MessageLogger' in process.__dict__:
        process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.limit = 10000000
    process.MessageLogger.cerr.FwkReport.reportEvery = reportEveryNEvents

    # change the source
    process.source.fileNames = inputFiles

    return process

def run(
        saveLogs = True):
    cmd = ('cmsRun', 'cfg.py')
    env = os.environ.copy()
    print("Starting to run: ", cmd)
    job = subprocess.Popen(cmd, cwd=os.getcwd(), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = job.communicate()

    if saveLogs:
        with open("logs.stdout", "w") as f:
            f.write(out)
        with open("logs.stderr", "w") as f:
            f.write(err)

    # make sure the job finished properly
    if job.returncode < 0:
        print("The job was killed by signal %d" % -job.returncode)
        return None
    elif job.returncode > 0:
        print("The job failed with return code %d" % job.returncode)
        return None
    elif job.returncode == 0:
        print("The job completed successfully")

    # usually MessageLogger is configured to write to stderr
    return err

def dumpPythonConf(process):
    with open("cfg.py", "w") as f:
        f.write(process.dumpPython())

#
# we assume here that we are already in some working directory from where everything 
# will be run and where the logs will be stored
# 
def main():
    # cli args
    # TODO better cli handling for things that could be varied from cli
    config = sys.argv[1]
    threads = int(sys.argv[2])
    data = sys.argv[3:]

    # overwrite from cli the number of threads to use
    optionsExtra["threads"] = threads
    optionsExtra["streams"] = threads

    # this is our cms process object extracted from the provided cfg
    process = parseCmsCfg(config)

    # apply extra settings
    process = applyExtraSettings(process, inputFiles=data, **optionsExtra)

    # dump the config to emulate `cmsRun cfg.py`
    dumpPythonConf(process)

    # run 
    logs = run(**optionsCmsRun)

if __name__ == "__main__":
    if not 'CMSSW_BASE' in os.environ:
        print("CMSSW_BASE env variable is not set but required")
        sys.exit(1)

    if len(sys.argv) == 1:
        print("usage:")
        print("python benchmark < path to config > < list of input files >" )
        sys.exit(1)

    main()
