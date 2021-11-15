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
# %%
# the avg enrollment day from RA start 3.55
treat_df['AutoLastEffectiveDay'].mean()/ 365.25
# %%
