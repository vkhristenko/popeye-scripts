#!/bin/bash

#SBATCH --partition=preempt
#SBATCH --qos=preempt
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --wait-all-nodes=1
#SBATCH --job-name=cmssw_m2n_iobench
#SBATCH --time=02:00:00
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
#DATADIR=/mnt/sdceph/users/vkhristenko/data/miniaod/iotests2
#for i in `seq 0 ${SLURM_NTASKS_PER_NODE}`;
#do
#    echo $i
#    cp $DATADIR/test.root $DATADIR/test_${i}.${SLURM_JOB_ID}.root
#done

# run the stuff on each node for each task/exe
srun run_cmsNano_recordnetstats_wrapper.sh $LOGSDIR_JOB $NUM_CORES $DATADIR

# clean up the 
#rm $DATADIR/test_*.root
