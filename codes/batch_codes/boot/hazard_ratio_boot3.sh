#!/bin/bash
COMMANDS=(
    "Malignant neoplasm of trachea")
for cancer_desc in "${COMMANDS[@]}"; do 
echo "${cancer_desc}"
#
export cancer_desc
#
sbatch -o output_txt/hazard_ratio_${cancer_desc:0:3}.stdout.txt \
-e err/hazard_ratio_${cancer_desc:0:3}.stdout.txt \
--job-name=hazard_ratio_${cancer_desc:0:3} \
batch_codes/boot/hazard_ratio_boot_run.sh
#
sleep 1 # pause to be kind to the scheduler
done