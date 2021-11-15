'''
Given some icd list as the autoimmune event type, output the HR to csv
'''
# %%
import pandas as pd
import sys
from helper import get_survival_both
import pickle
from useful_chunk import create_dir

# %%
# read data
treat_df = pd.read_pickle('../data/treat_data_RA.pkl')
control_df = pd.read_pickle('../data/control_data_RA.pkl')
# control_df = pd.read_pickle('../data/potential_data/treat_data_final.pkl')
# %%
# print(sys.argv)
# assert(len(sys.argv) == 2)
# if len(sys.argv) == 2:
#     cancer_desc = sys.argv[1]
# else:
#     cancer_desc = 'colo-rectum'
cancer_desc = " ".join(sys.argv[1:])

# assume the root folder is at codes/
with open('batch_codes/parameter_setting/{}.pickle'.format(cancer_desc), 'rb') as f:
        cancer_icd_list, _ = pickle.load(f)

treat_survival_df, control_survival_df = \
    get_survival_both(treat_df, control_df, cancer_icd_list, cancer_desc)

# %%
create_dir("../output_data/survival_analysis")
with open(f'../output_data/survival_analysis/{cancer_desc}.pickle', 'wb') as f:
    pickle.dump((cancer_icd_list, cancer_desc, treat_survival_df, control_survival_df), f)

# %%

# # cancer types we interested in
# cancer_dict = {}
# cancer_dict[('C33', 'C34', '162')] = 'Lung'
# cancer_dict[('C81', '201')] = "Hodgkin's lymphoma"
# cancer_dict[tuple([f'C{num}' for num in range(82, 89)] + ['200'])] = \
#     "Nonhodgkin's lymphoma"
# cancer_dict[tuple([f'C{num}' for num in range(91, 96)] + 
#     [f'{num}' for num in range(204, 209)])] = "Leukemia"
# cancer_dict
# %%
