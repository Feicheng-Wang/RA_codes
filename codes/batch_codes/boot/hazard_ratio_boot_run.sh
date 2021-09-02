#!/bin/bash
#SBATCH -n 8 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 0-08:00 # Runtime in D-HH:MM
#SBATCH -p shared,serial_requeue,janson,janson_bigmem,janson_cascade # Partition to submit to
#SBATCH --mem=40000 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o output_txt/hostname_%j.out # File to which STDOUT will be written
#SBATCH -e err/hostname_%j.err # File to which STDERR will be written

hostname

module load python

python ./step1_survival_analysis_event_icd.py ${cancer_desc} 
python ./step2_boot_HR.py ${cancer_desc} 

