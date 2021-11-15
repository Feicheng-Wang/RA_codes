#!/bin/bash
COMMANDS=("Malignant neoplasm of nasal cavities, middle ear and accessory sinuses" \
    "Malignant neoplasm of larynx" \
    "Malignant neoplasm of trachea, bronchus and lung" \
    "Malignant neoplasm of other and ill-defined sites within the respiratory system and intrathoracic organs" \
    "Lymphosarcoma and reticulosarcoma" \
    "Hodgkin's disease" \
    "Other malignant neoplasms of lymphoid and histiocytic tissue" \
    "Multiple myeloma and immunoproliferative neoplasms" \
    "Lymphoid leukemia" \
    "Myeloid leukemia" \
    "Monocytic leukemia" \
    "Other specified leukemia" \
    "Leukemia of unspecified cell type")
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