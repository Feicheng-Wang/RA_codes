'''
Given some icd list as the autoimmune event type, output the HR to csv
'''
# %%
import pandas as pd
import sys
from helper import get_survival_both
import pickle

# %%
# read data
treat_df = pd.read_pickle('../data/treat_data_RA.pkl')
control_df = pd.read_pickle('../data/control_data_RA.pkl')
# %%
if len(sys.argv) == 2:
    cancer_desc = sys.argv[1]
else:
    cancer_desc = 'colo-rectum'

# assume the root folder is at codes/
with open('batch_codes/parameter_setting/{}.pickle'.format(cancer_desc), 'rb') as f:
        cancer_icd_list, _ = pickle.load(f)

treat_survival_df, control_survival_df = \
    get_survival_both(treat_df, control_df, cancer_icd_list, cancer_desc)

# %%
with open(f'../output_data/{cancer_desc}.pickle', 'wb') as f:
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
