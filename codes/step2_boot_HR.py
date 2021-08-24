# %%
import pickle

from useful_chunk import create_dir
from helper import cal_survival_risk 
import numpy as np
import sys

# disable chained assignments
import pandas as pd

# %%
if len(sys.argv) == 2:
    cancer_desc = sys.argv[1]
else:
    cancer_desc = 'colo-rectum'

# assume the root folder is at codes/
with open('batch_codes/parameter_setting/{}.pickle'.format(cancer_desc), 'rb') as f:
        cancer_icd_list, _ = pickle.load(f)

with open(f'../output_data/{cancer_desc}.pickle', 'rb') as f:
    (cancer_icd_list, cancer_desc, 
        treat_survival_df, control_survival_df) = pickle.load(f)

i = 1234
import random
random_seed = i
random.seed(random_seed)

# %%
repeat = 1000
df_list = []

# fig, ax = plt.subplots(figsize=(24, 12))
def bootstrap_df(data):
    n = len(data)
    out = data.iloc[np.random.randint(n, size=n)]
    return out

time_list = [10, 30, 90, 180, 365, 1000]
n_time = len(time_list)
for iter_num in range(repeat):
    HR_array = np.zeros(n_time)
    treat_survival_df_boot = bootstrap_df(treat_survival_df)
    control_survival_df_boot = bootstrap_df(control_survival_df)
    
    auto_risk_dict = cal_survival_risk(treat_survival_df_boot, time_list)
    nonauto_risk_dict = cal_survival_risk(control_survival_df_boot, time_list)
    for i, time in enumerate(time_list):
        HR_array[i] = np.round(
            float(auto_risk_dict[time]/nonauto_risk_dict[time]), 3)

    tmp_df = pd.DataFrame()
    tmp_df['hazard_ratio'] = HR_array
    tmp_df['time_in_days'] = time_list
    tmp_df['repeat'] = iter_num
    tmp_df['cancer_desc'] = cancer_desc
    tmp_df['random_seed'] = random_seed
    df_list.append(tmp_df)

df = pd.concat(df_list, axis = 0)
# df
# %%
create_dir("../output_data/boot_HR")
with open(f'../output_data/boot_HR/RA-cancer_desc_{cancer_desc}-randomseed_{random_seed}.pickle', 'wb') as f:
    pickle.dump(df, f)

# %%
# with open(f'output/boot_HR/RA-randomseed{random_seed}.pickle', 'rb') as handle:
#     df = pickle.load(handle)

# %%
