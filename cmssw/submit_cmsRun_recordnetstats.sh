#!/bin/bash

#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks=6
#SBATCH --cpus-per-task=8
#SBATCH --wait-all-nodes=1
#SBATCH --job-name=cmssw_m2n_iobench
#SBATCH --time=01:00:00
#SBATCH --output=/home/vkhristenko/jobs_results/submission_logs/%j.log
#SBATCH --error=/home/vkhristenko/jobs_results/submission_logs/%j.err

# general settings
LOGSDIR_TOP=/home/vkhristenko/jobs_results/job_logs
NUM_CORES=$SLURM_CPUS_PER_TASK

# based on the above
LOGSDIR_JOB="$LOGSDIR_TOP/job_$SLURM_JOB_ID"

# create a common dir for this job for the logs/results
[ -d "$LOGSDIR_JOB" ] && rm -rf "$LOGSDIR_JOB"
mkdir $LOGSDIR_JOB

# rotate input data
DATADIR=/mnt/sdceph/users/vkhristenko/data/miniaod/iotests
for i in `seq 0 10`;
do
    echo $i
    cp $DATADIR/test.root $DATADIR/test_${i}.${SLURM_JOB_ID}.root
done

# run the stuff on each node for each task/exe
srun run_cmsRun_recordnetstats_wrapper.sh $LOGSDIR_JOB $NUM_CORES $DATADIR

# clean up the 
rm $DATADIR/test_*.root
