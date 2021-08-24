#!/bin/bash
COMMANDS=("all_cancers" "lip, oral cavity, and pharynx" "digestive organs" \
    "respiratory and intrathoracic organs" "bone and articular cartilage" \
    "skin" "soft tissue" "Kaposi's sarcoma" "breast" "female genital organs" \
    "male genital organs" "urinary tract" \
    "eye, brain and other parts of central nervous system" \
    "thyroid and other endocrine glands" \
    "ill-defined, other secondary and unspecified sites" \
    "neuroendocrine tumors" "lymphoid and hematopoietic tissue")
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


    # 'all_cancers': [],
    # 'colo-rectum': ['C17','C18','C19','C20'],
    # 'lip, oral cavity, and pharynx': [f"C{i:02}" for i in range(15)] + 
    #     [str(i) for i in range(140,149+1)],
    # "digestive organs": [f"C{i:02}" for i in range(15, 26)] + 
    #     [str(i) for i in range(150,159+1)], 
    # "respiratory and intrathoracic organs": [f"C{i:02}" for i in range(30, 40)] + 
    #     [str(i) for i in range(160,165+1)], 
    # "bone and articular cartilage": ['C40', 'C41'] + 
    #     ['170'], 
    # "skin": ['C43', 'C44'] + 
    #     ['172', '173'],
    # "soft tissue": ['C49'] + ['171'],
    # "Kaposi's sarcoma": ['C46'] + ['176'],
    # "breast": ['C50'] + ['174', '175'],
    # "female genital organs": [f"C{i:02}" for i in range(51, 59)] + 
    #     [str(i) for i in range(179,184+1)],
    # "male genital organs": [f"C{i:02}" for i in range(60, 64)] + 
    #     [str(i) for i in range(185,187+1)],
    # "urinary tract": [f"C{i:02}" for i in range(64, 69)] + 
    #     [str(i) for i in range(188,189+1)],
    # "eye, brain and other parts of central nervous system": \
    #     [f"C{i:02}" for i in range(69, 73)] + [str(i) for i in range(190,192+1)],
    # "thyroid and other endocrine glands": [f"C{i:02}" for i in range(73, 75+1)] +
    #     [str(i) for i in range(193,194+1)],
    # "ill-defined, other secondary and unspecified sites":\
    #     [f"C{i:02}" for i in range(76, 80+1)] + 
    #         [str(i) for i in range(195, 199+1)],
    # "neuroendocrine tumors": ['C7A', 'C7B'] + 
    #     ['209'],
    # "lymphoid and hematopoietic tissue": ['C81-C96'] + 
    #     [str(i) for i in range(200, 208+1)]