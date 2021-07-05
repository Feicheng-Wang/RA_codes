#%%
import pandas as pd 
import pickle
import os

# %%
'''
criteria for cancer in icd 9
'140' - '239'
criteria for cancer in icd 10
begin with C
okay let's now create a table for these!
'''

icd10_dict = {
    "C00-C14": "lip, oral cavity, and pharynx",
    "C15-C26": "digestive organs",
    "C30-C39": "respiratory and intrathoracic organs",
    "C40-C41": "bone and articular cartilage",
    "C43-C44": "skin",
    "C45-C49": "soft tissue",
    "C46-C46": "Kaposi's sarcoma", # one special case
    "C50-C50": "breast",    
    "C51-C58": "female genital organs",-
    "C60-C63": "male genital organs",
    "C64-C68": "urinary tract",
    "C69-C72": "eye, brain and other parts of central nervous system",
    "C73-C75":  "thyroid and other endocrine glands",
    "C76-C80":  "ill-defined, other secondary and unspecified sites",
    "C7A-C7A": "neuroendocrine tumors",
    "C7B-C7B":  "neuroendocrine tumors",
    "C81-C96": "lymphoid and hematopoietic tissue"
}
icd9_dict = {
    "140-149": "Lip, Oral Cavity, And Pharynx",
    "150-159": "Digestive Organs",
    "160-165": "Respiratory And Intrathoracic Organs",
    # "170-176":  "Bone, Connective Tissue, Skin, And Breast",
    "170-170": "bone and articular cartilage",
    "171-171": "soft tissue",
    "172-173": "skin",
    "174-175": "breast",
    "176-176": "Kaposi's sarcoma",
    # "179-189":  "Genitourinary Organs",
    "179-184": "female genital organs",
    "185-187": "male genital organs",
    "188-189": "urinary tract",
    # "190-199": "Other And Unspecified Sites",
    "190-192": "eye, brain and other parts of central nervous system",
    "193-194": "thyroid and other endocrine glands",
    "195-199": "ill-defined, other secondary and unspecified sites",
    "200-208":  "Lymphoid And Hematopoietic Tissue",
    "209-209": "neuroendocrine tumors",
    "210-239": "Benign Neoplasms and uncertain behaviors (only icd10)"
    # "210-229": "Benign Neoplasms",
    # "230-234":  "Carcinoma In Situ",
    # "235-238": "Neoplasms Of Uncertain Behavior",
    # "239-239":  "Neoplasms Of Unspecified Nature"
}
#%%
def generate_icd_description(icd10_dict, icd9_dict, icd_data_savepath, 
    icd_desc_savepath, header_icd = False):
    '''
        Purpose:
            Use icd9 and icd10 data dict create a table
        Input:
            icd10_dict: Like "C81-C96": "lymphoid and hematopoietic tissue"
            icd9_dict: Similar to icd10_dict
            icd_data_savepath: the save path for output clean dataframe 
                with cancer icd description
            icd_desc_savepath: "output/desc_choice.pkl"
            header_icd: if True, add icd code in front of desc
                like from lymphoid and hematopoietic tissue
                to C81 lymphoid and hematopoietic tissue
        Output:
            dataframe with 
            C81 lymphoid and hematopoietic tissue
            C82 lymphoid and hematopoietic tissue
            ...
            C96 lymphoid and hematopoietic tissue
    '''
    def reform_dict(input_dict):
        '''
        reform input_dict like "C81-C96": "lymphoid and hematopoietic tissue"
        into output dataframe like:
            C81 lymphoid and hematopoietic tissue
            C82 lymphoid and hematopoietic tissue
            ...
            C96 lymphoid and hematopoietic tissue
        '''
        reformed_dict = {}
        for key, item in input_dict.items():
            # if key len = 3, means it looks like Cxx or 1xx 2xx, which is itself a key
            if len(key) == 3:
                reformed_dict[key] = item.lower()
            # else the key is like xxx-xxx, which can be separated into two parts
            else:
                begin = key[1:3]
                end = key[-2:]
                # assess if str can be interpreted as digit
                # if True: iterate all keys between begin and end digits
                if begin.isdigit() and end.isdigit(): 
                    for word in range(int(begin), int(end)+1):
                        word = str(word)
                        if len(word) == 1:
                            # word = "C0" + word
                            word = str(key[0]) + str(0) + word
                        elif len(word) == 2:
                            # word = "C" + word
                            word = str(key[0]) + word
                        else:
                            exit("word length not correct!!!")
                        reformed_dict[word] = item.lower()
                else:
                    # for now this only contains 7A and 7B, so it's straight forward
                    reformed_dict["C" + begin] = item.lower()

        if header_icd is True:
            tmp = {}
            for key, item in reformed_dict.items():
                tmp[key] = key + " " + item
            reformed_dict = tmp

        reformed_dict2 = {'icd':[], 'description':[]}
        for key, item in reformed_dict.items():
            reformed_dict2['icd'].append(key)
            reformed_dict2['description'].append(item)
        
        # finally get output in a df form
        output_df = pd.DataFrame(data=reformed_dict2)

        return(output_df)

    # two formatted df with icd class and description
    icd10_data = reform_dict(icd10_dict)
    icd10_data['icd_type'] = 10
    icd9_data = reform_dict(icd9_dict)
    icd9_data['icd_type'] = 9


    icd_data = pd.concat([icd10_data,icd9_data], axis=0)
    icd_data = icd_data.reset_index()

    icd_data.to_csv(icd_data_savepath)

    desc_choice = icd_data['description'].unique()
    for desc in desc_choice:
        print(desc, len(icd_data[icd_data['description'] == desc]["icd_type"].unique()))

    print(os.getcwd)
    with open(icd_desc_savepath, 'wb') as f:
        pickle.dump(desc_choice, f)

# %%
os.chdir('../odyssey_code')
generate_icd_description(icd10_dict, icd9_dict, "../output/icd_data.csv", 
    "../output/desc_choice.pkl", header_icd = False)
# %%
