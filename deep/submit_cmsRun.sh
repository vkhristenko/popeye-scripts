#!/bin/bash

#SBATCH --partition=dp-cn
#SBATCH -A deep
#SBATCH --nodes=49
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=4
#SBATCH --wait-all-nodes=1
#SBATCH --job-name=cmssw_m2n_iobench
#SBATCH --time=01:00:00
#SBATCH --output=/work/cdeep/khristenko1/jobs_results/submission_logs/%j.log
#SBATCH --error=/work/cdeep/khristenko1/jobs_results/submission_logs/%j.err

# general settings
LOGSDIR_TOP=/work/cdeep/khristenko1/jobs_results/job_logs
NUM_CORES=$SLURM_CPUS_PER_TASK
VARYINPUT=1

# based on the above
LOGSDIR_JOB="$LOGSDIR_TOP/job_$SLURM_JOB_ID"

# create a common dir for this job for the logs/results
[ -d "$LOGSDIR_JOB" ] && rm -rf "$LOGSDIR_JOB"
mkdir $LOGSDIR_JOB

# rotate input data
#DATADIR=/p/project/cdeep/khristenko1/data/opendata/260000/allfeds_moreevents/
DATADIR=/work/cdeep/khristenko1/data/opendata/260000/allfeds_moreevents
if [ $VARYINPUT -eq 1 ]
then
    for i in `seq 0 ${SLURM_NTASKS_PER_NODE}`;
    do
        echo $i
        [ -d "$DATADIR/tests/${i}_${SLURM_JOB_ID}" ] && rm -rf $DATADIR/tests/${i}_${SLURM_JOB_ID}
        mkdir $DATADIR/tests/${i}_${SLURM_JOB_ID}
        cp -r $DATADIR/run260000/*ls0010* $DATADIR/tests/${i}_${SLURM_JOB_ID}/
    done
else
    for i in 0;
    do
        echo $i
        [ -d "$DATADIR/tests/${i}_${SLURM_JOB_ID}" ] && rm -rf $DATADIR/tests/${i}_${SLURM_JOB_ID}
        mkdir $DATADIR/tests/${i}_${SLURM_JOB_ID}
        cp -r $DATADIR/run260000/*ls0010* $DATADIR/tests/${i}_${SLURM_JOB_ID}/
    done
fi

# run the stuff on each node for each task/exe
srun run_cmsRun_wrapper.sh $LOGSDIR_JOB $NUM_CORES $DATADIR/tests $VARYINPUT

# clean up
rm -rf $DATADIR/tests/*
