'''
Given some icd list as the autoimmune event type, output the HR to csv
'''
# %%
import pandas as pd
from helper import get_survival_both

# %%
# read data
treat_df = pd.read_pickle('../data/treat_data_RA.pkl')
control_df = pd.read_pickle('../data/control_data_RA.pkl')
# %%
cancer_icd_list = ['C17','C18','C19','C20']
cancer_desc = 'Colo-rectum'
treat_survival_df, control_survival_df = \
    get_survival_both(treat_df, control_df, cancer_icd_list, cancer_desc)


# %%
