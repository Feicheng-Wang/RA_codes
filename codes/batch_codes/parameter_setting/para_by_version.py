# %% 
# import packges
import pickle

# %%
cancer_icd_list = ['C17','C18','C19','C20']
cancer_desc = 'colo-rectum'

with open('parameter_setting/{}.pickle'.format(cancer_desc), 'wb') as f:
    pickle.dump((cancer_icd_list, cancer_desc), f)

# %%
cancer_dict = {
    'all_cancers': [],
    'colo-rectum': ['C17','C18','C19','C20'],
    'lip, oral cavity, and pharynx': [f"C{i:02}" for i in range(15)] + 
        [str(i) for i in range(140,149+1)],
    "digestive organs": [f"C{i:02}" for i in range(15, 26)] + 
        [str(i) for i in range(150,159+1)], 
    "respiratory and intrathoracic organs": [f"C{i:02}" for i in range(30, 40)] + 
        [str(i) for i in range(160,165+1)], 
    "bone and articular cartilage": ['C40', 'C41'] + 
        ['170'], 
    "skin": ['C43', 'C44'] + 
        ['172', '173'],
    "soft tissue": ['C49'] + ['171'],
    "Kaposi's sarcoma": ['C46'] + ['176'],
    "breast": ['C50'] + ['174', '175'],
    "female genital organs": [f"C{i:02}" for i in range(51, 59)] + 
        [str(i) for i in range(179,184+1)],
    "male genital organs": [f"C{i:02}" for i in range(60, 64)] + 
        [str(i) for i in range(185,187+1)],
    "urinary tract": [f"C{i:02}" for i in range(64, 69)] + 
        [str(i) for i in range(188,189+1)],
    "eye, brain and other parts of central nervous system": \
        [f"C{i:02}" for i in range(69, 73)] + [str(i) for i in range(190,192+1)],
    "thyroid and other endocrine glands": [f"C{i:02}" for i in range(73, 75+1)] +
        [str(i) for i in range(193,194+1)],
    "ill-defined, other secondary and unspecified sites":\
        [f"C{i:02}" for i in range(76, 80+1)] + 
            [str(i) for i in range(195, 199+1)],
    "neuroendocrine tumors": ['C7A', 'C7B'] + 
        ['209'],
    "lymphoid and hematopoietic tissue": ['C81-C96'] + 
        [str(i) for i in range(200, 208+1)]
}
for cancer_desc, cancer_icd_list in cancer_dict.items():
    with open('parameter_setting/{}.pickle'.format(cancer_desc), 'wb') as f:
        pickle.dump((cancer_icd_list, cancer_desc), f)
# %%
# "140-149": "Lip, Oral Cavity, And Pharynx",
# "150-159": "Digestive Organs",
# "160-165": "Respiratory And Intrathoracic Organs",
# "170-170": "bone and articular cartilage",
# "171-171": "soft tissue",
# "172-173": "skin",
# "174-175": "breast",
# "176-176": "Kaposi's sarcoma",
# "179-184": "female genital organs",
# "185-187": "male genital organs",
# "188-189": "urinary tract",
# "190-192": "eye, brain and other parts of central nervous system",
# "193-194": "thyroid and other endocrine glands",
# "195-199": "ill-defined, other secondary and unspecified sites",
# "200-208":  "Lymphoid And Hematopoietic Tissue",
# "209-209": "neuroendocrine tumors",
# "210-239": "Benign Neoplasms and uncertain behaviors (only icd9)"

# "C00-C14": "lip, oral cavity, and pharynx",
# "C15-C26": "digestive organs",
# "C30-C39": "respiratory and intrathoracic organs",
# "C40-C41": "bone and articular cartilage",
# "C43-C44": "skin",
# "C49": "soft tissue",
# "C46-C46": "Kaposi's sarcoma", # one special case
# "C50-C50": "breast",    
# "C51-C58": "female genital organs",-
# "C60-C63": "male genital organs",
# "C64-C68": "urinary tract",
# "C69-C72": "eye, brain and other parts of central nervous system",
# "C73-C75":  "thyroid and other endocrine glands",
# "C76-C80":  "ill-defined, other secondary and unspecified sites",
# "C7A-C7A": "neuroendocrine tumors",
# "C7B-C7B":  "neuroendocrine tumors",
# "C81-C96": "lymphoid and hematopoietic tissue"
# %%
with open('parameter_setting/{}.pickle'.format(cancer_desc), 'rb') as f:
    (cancer_icd_list, cancer_desc) = pickle.load(f)
(cancer_icd_list, cancer_desc)
# %%
