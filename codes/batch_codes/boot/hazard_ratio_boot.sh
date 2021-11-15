#!/bin/bash
COMMANDS=("all_cancers" "lip, oral cavity, and pharynx" "digestive organs" \
    "respiratory and intrathoracic organs" "bone and articular cartilage" \
    "skin" "soft tissue" "Kaposi's sarcoma" "breast" "female genital organs" \
    "male genital organs" "urinary tract" \
    "eye, brain and other parts of central nervous system" \
    "thyroid and other endocrine glands" \
    "ill-defined, other secondary and unspecified sites" \
    "neuroendocrine tumors" "lymphoid and hematopoietic tissue" "colo-rectum")
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
