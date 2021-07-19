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
CMSRELEASE=/home/vkhristenko/cmssw_releases/nanoaod_analysis/CMSSW_10_2_18/src
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

# grid/voms certs are in non-standard location
export X509_USER_PROXY=/mnt/home/vkhristenko/out_voms
export LD_LIBRARY_PATH=$CMSRELEASE/PhysicsTools/NanoAODTools:$LD_LIBRARY_PATH

# copy the data to the local disk
#cp $DATADIR/test.root $WORKDIR/input_test.root

#DATAFILES="file:${DATADIR}/test_${INSTANCE}.${SLURM_JOB_ID}.root"
#DATAFILES="${DATADIR}/test_${INSTANCE}.${SLURM_JOB_ID}.root"
#DATAFILES="file:${WORKDIR}/input_test.root"
#DATAFILES="root://cmsxrootd.fnal.gov//store/mc/RunIIAutumn18MiniAOD/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/10000/02CDAB0B-7ED5-7246-AE11-9C3B953C0E8B.root"
#DATAFILES="root://xcache-redirector-real.t2.ucsd.edu:2040//store/mc/RunIIAutumn18MiniAOD/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/10000/02CDAB0B-7ED5-7246-AE11-9C3B953C0E8B.root"
DATAFILES="root://xcache-redirector-real.t2.ucsd.edu:2040//store/data/Run2018D/SingleMuon/NANOAOD/02Apr2020-v1/230000/01832F27-F3C8-6A4E-A080-52FF99C0AE57.root"

ifconfig > logs.test

# run cmsRun for instance 0
if [ $INSTANCE -eq 0 ]
then
    python $CMSRELEASE/PhysicsTools/NanoAODTools/scripts/nano_postproc.py ./ $DATAFILES -b $CMSRELEASE/PhysicsTools/NanoAODTools/python/postprocessing/examples/keep_and_drop.txt -I PhysicsTools.NanoAODTools.postprocessing.examples.vbsHwwSkimModule vbsHwwSkimModuleConstr > logs.stdout 2>logs.stderr &

    # loop and collect network usage 
    # break out when the aboe process is finished
    PID=$!
    while true;
    do
        [ -n "${PID}" -a -d "/proc/${PID}" ] || break
        timestamp=`date --rfc-3339=seconds`
        bytes_ib0=`cat /sys/class/net/ib0/statistics/rx_bytes`
        bytes_eno1=`cat /sys/class/net/eno1/statistics/rx_bytes`
        bytes_eno2=`cat /sys/class/net/eno2/statistics/rx_bytes`
        echo "$timestamp $bytes_ib0" >> ib0.netlogs
        echo "$timestamp $bytes_eno1" >> eno1.netlogs
        echo "$timestamp $bytes_eno2" >> eno2.netlogs
        mpstat -P ALL 1 1 >> cpuutillogs
        sleep 1
    done

    # save the net logs
    mv ib0.netlogs eno1.netlogs eno2.netlogs $LOGSDIR_TASK/
    mv cpuutillogs $LOGSDIR_TASK/
else
    # for all the other instances
    python $CMSRELEASE/PhysicsTools/NanoAODTools/scripts/nano_postproc.py ./ $DATAFILES -b $CMSRELEASE/PhysicsTools/NanoAODTools/python/postprocessing/examples/keep_and_drop.txt -I PhysicsTools.NanoAODTools.postprocessing.examples.vbsHwwSkimModule vbsHwwSkimModuleConstr > logs.stdout 2>logs.stderr
fi

# move the logs if exist
ifconfig >> logs.test
mv logs.stderr logs.stdout $LOGSDIR_TASK/
mv logs.test $LOGSDIR_TASK/
