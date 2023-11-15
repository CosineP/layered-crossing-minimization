#!/bin/bash
#SBATCH -J FixedDensityExperiment               # Job name
#SBATCH -N 1                   # Number of nodes
#SBATCH -n 1                  # Number of tasks
#SBATCH --time 24:00:00
#SBATCH --constraint=broadwell
#SBATCH --mem=8G
#SBATCH -o outputs/fixeddens_%A_%a.txt       # Standard output file
#SBATCH -e errors/fixeddens_%A_%a.txt        # Standard error file

module load gurobi
srun python experiments.py 4 $SLURM_ARRAY_TASK_ID
