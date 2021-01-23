#!/bin/bash

# cli
LOGSDIR_JOB=$1
NUM_CORES=$2
DATADIR=$3

THISHOST="`hostname`"
INSTANCE=$SLURM_LOCALID

# various variables
WORKDIR="/tmp/cmsrun__$INSTANCE"
LOGSDIR_TASK="$LOGSDIR_JOB/${THISHOST}__$INSTANCE"
CMSRELEASE=/home/vkhristenko/cmssw_releases/CMSSW_10_2_18/src
CMSRUN_CFG=~/cmssw_configs/mini2nano_2018_ttjets.py

# cms env
source /home/vkhristenko/cms_env.sh
cd $CMSRELEASE
eval `scramv1 runtime -sh`

# create the logs directory 
[ -d "$LOGSDIR_TASK" ] && echo "$LOGSDIR_TASK already exists!!!" && exit 1
mkdir $LOGSDIR_TASK

# create a working directly on the node
[ -d "$WORKDIR" ] && rm -rf $WORKDIR
mkdir $WORKDIR
cd $WORKDIR

DATAFILES="file:${DATADIR}/test_${INSTANCE}.${SLURM_JOB_ID}.root"

# run cmsRun
python2 /home/vkhristenko/popeye-scripts/cmssw/run_cmsRun.py $CMSRUN_CFG $NUM_CORES $DATAFILES

# move the logs if exist
mv logs.stdout logs.stderr $LOGSDIR_TASK/
