#!/bin/bash

#SBATCH --partition=general
#SBATCH --nodes=5
#SBATCH --cpus-per-task=8
#SBATCH --job-name=cmssw_m2n_iobench
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=viktor.khristenko@cern.ch
#SBATCH --time=01:00:00
#SBATCH --output=/home/vkhristenko/jobs_results/submission_logs/%j.log
#SBATCH --error=/home/vkhristenko/jobs_results/submission_logs/%j.err

echo "job id: $SLURM_JOB_ID"
echo "job node list: $SLURM_JOB_NODELIST"
echo "cpus per task: $SLURM_CPUS_PER_TASK"
