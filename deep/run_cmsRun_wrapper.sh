#!/bin/bash

# cli
LOGSDIR_JOB=$1
NUM_CORES=$2
DATADIR=$3
VARYINPUT=$4

THISHOST="`hostname`"
INSTANCE=$SLURM_LOCALID

# various variables
WORKDIR="/tmp/cmsrun__$INSTANCE"
LOGSDIR_TASK="$LOGSDIR_JOB/${THISHOST}__$INSTANCE"
#CMSRELEASE=/home/vkhristenko/cmssw_releases/CMSSW_10_2_18/src
CMSRELEASE=/p/project/cdeep/khristenko1/cmssw_releases/cmssoft_releases/CMSSW_11_1_3_Patatrack/src/
#CMSRUN_CFG=~/cmssw_configs/mini2nano_2018_ttjets.py
CMSRUN_CFG=/p/project/cdeep/khristenko1/cmsrun_configs/opendata_hlt/hlt_rawinput_cpu.py

# cms env
source /p/project/cdeep/khristenko1/cms_env.sh
cd $CMSRELEASE
eval `scramv1 runtime -sh`

# create the logs directory 
[ -d "$LOGSDIR_TASK" ] && echo "$LOGSDIR_TASK already exists!!!" && exit 1
mkdir $LOGSDIR_TASK

# create a working directly on the node
[ -d "$WORKDIR" ] && rm -rf $WORKDIR
mkdir $WORKDIR
cd $WORKDIR

#DATAFILES="file:${DATADIR}/test_${INSTANCE}.${SLURM_JOB_ID}.root"
if [ $VARYINPUT -eq 1 ]
then
    DATAFILES=`ls ${DATADIR}/${INSTANCE}_${SLURM_JOB_ID}/*.raw`
else
    DATAFILES=`ls ${DATADIR}/0_${SLURM_JOB_ID}/*.raw`
fi

# run cmsRun
python2 /p/project/cdeep/khristenko1/popeye-scripts/deep/run_cmsRun.py $CMSRUN_CFG $NUM_CORES $DATAFILES
mv logs.stderr logs.stderr.full
head -5000 logs.stderr.full > logs.stderr

# move the logs if exist
mv logs.stdout logs.stderr $LOGSDIR_TASK/
