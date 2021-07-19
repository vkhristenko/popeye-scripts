#!/bin/bash

#SBATCH --partition=preempt 
#SBATCH --qos=preempt 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --wait-all-nodes=1
#SBATCH --job-name=cmssw_m2n_iobench
#SBATCH --time=20:00
#SBATCH --output=/home/vkhristenko/jobs_results/submission_logs/%j.log
#SBATCH --error=/home/vkhristenko/jobs_results/submission_logs/%j.err

srun exec.sh
