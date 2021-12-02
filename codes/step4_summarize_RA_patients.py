# # %%
# import pandas as pd
# import sys
# from helper import get_survival_both
# import pickle
# from useful_chunk import create_dir

# # %%
# # read data
# treat_df = pd.read_pickle('../data/treat_data_RA.pkl')
# control_df = pd.read_pickle('../data/control_data_RA.pkl')
# # %%
# # the avg enrollment day from RA start 3.55
# treat_df['AutoLastEffectiveDay'].mean()/ 365.25
# # %%


# %%
import pandas as pd

df = pd.read_pickle('../output_data/focus_HR_summary.pickle')
df.loc[df['time_in_days'] == 365, ['cancer_desc', 'cancer_count', 'expression']]\
    .sort_values('cancer_count', ascending=False)
# %%
