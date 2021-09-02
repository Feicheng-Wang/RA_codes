'''
Plot HR as bars (default at 365 days)
'''
# %%
import pandas as pd
# from helper import get_survival_both
import numpy as np
from helper import cal_survival_risk 
from useful_chunk import create_dir
import matplotlib.pyplot as plt
import seaborn as sns
# %%
cancer_desc = "skin"
random_seed = 1234

df_list = []
for cancer_desc in ["all_cancers", "lip, oral cavity, and pharynx", "digestive organs", \
    "respiratory and intrathoracic organs", "bone and articular cartilage", \
    "skin", "soft tissue", "Kaposi's sarcoma", "breast", "female genital organs", \
    "male genital organs", "urinary tract", \
    "eye, brain and other parts of central nervous system", \
    "thyroid and other endocrine glands", \
    "ill-defined, other secondary and unspecified sites", \
    "neuroendocrine tumors", "lymphoid and hematopoietic tissue"]:
    ###
    df = pd.read_pickle(f'../output_data/boot_HR/\
RA-cancer_desc_{cancer_desc}-randomseed_{random_seed}.pickle')

    # distill the upper and lower
    df = df.dropna()
    tmp_df = df.groupby(['time_in_days', 'cancer_desc']).agg(
        {'hazard_ratio' : [('upper', lambda x: np.quantile(x, 0.975)), 
            ('lower', lambda x: np.nanquantile(x, 0.025))]
        })
    tmp_df.reset_index(inplace=True)
    tmp_df.columns = ['time_in_days', 'cancer_desc', 'upper', 'lower']
    df = tmp_df.copy()

    # cal the original value
    time_list = df.time_in_days.unique()
    _, _, treat_survival_df, control_survival_df = \
        pd.read_pickle(f'../output_data/survival_analysis/{cancer_desc}.pickle')

    HR_array = np.zeros(len(time_list))

    auto_risk_dict = cal_survival_risk(treat_survival_df, time_list)
    nonauto_risk_dict = cal_survival_risk(control_survival_df, time_list)
    for i, time in enumerate(time_list):
        HR_array[i] = np.round(
            float(auto_risk_dict[time]/nonauto_risk_dict[time]), 3)

    tmp_df = pd.DataFrame()
    tmp_df['hazard_ratio'] = HR_array
    tmp_df['time_in_days'] = time_list
    tmp_df['cancer_desc'] = cancer_desc
    tmp_df['cancer_count'] = treat_survival_df.cancerFlag.sum()

    df = df.merge(tmp_df, on=['cancer_desc', 'time_in_days'])
    df_list.append(df)

# merge all the data
df = pd.concat(df_list, axis=0)
# %%
# save the results
# df.to_pickle('../output_data/HR_summary.pickle')

for label in ['upper', 'lower', 'hazard_ratio']:
    df[label] = np.round(df[label], 2)
df.columns = ['time_in_days', 'cancer_desc', 'lower', 'upper', 'hazard_ratio', 'cancer_count']
df[['lower', 'upper']] = df[['upper', 'lower']] 

df[df['time_in_days'] == 365].sort_values('cancer_count', ascending=False)

# %%
df = df.sort_values('cancer_count', ascending=True)
N = len(df.cancer_desc.unique())
color_plate = sns.color_palette("husl", 7)

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)

time = 365
df = df[df.time_in_days == time]
df = df[df['upper'] != np.infty]
ind = np.arange(len(df))
ax.barh(ind, width = df.hazard_ratio, height=0.7, 
    xerr=[df.hazard_ratio - df['lower'], 
    df['upper'] - df.hazard_ratio],
    capsize=0, label=f"{time}-days", 
    color = color_plate[5])

plt.legend()
# ax.set_xticks(ind + width / 2, df.cancer_desc.unique())
plt.yticks(ind + width / 2, df.cancer_desc.unique())
max_height = 1 + np.nanmax(df['upper']) # ignore nan

plt.xlim(right = max_height - 0.6)
df_list.append(df)
plt.axvline(x=1, color="black")
plt.title(f"RA")
ax.set_xlabel(f"Matched patient count = {len(treat_survival_df)}")
create_dir('../output')
create_dir('../output/new_summary_fig')
# plt.savefig(f"output/new_summary_fig/time-{time}-RA_hazard_ratio_withCI.pdf", 
#     bbox_inches='tight') 
ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(20)
plt.xticks(fontsize= 20)
plt.yticks(fontsize= 20)
plt.legend(fontsize= 20)
ax.title.set_size(fontsize=20)
plt.savefig(f"../output/new_summary_fig/RA_hazard_ratio_withCI_time_{time}.pdf", 
    bbox_inches='tight')   



# %%
