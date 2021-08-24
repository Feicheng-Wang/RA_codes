'''
Plot HR as bars (default at 365 days)
'''
# %%
import pandas as pd
from helper import get_survival_both
import pickle

# %%
# For each auto, plot the bar of every cancer class's HR at 1500 days.
df_list = list()
# for subfolder_name in subfolder_names:
subfolder_name = '68415Rheumatoid arthritis'
folder_path = HOMEPATH + "/" + subfolder_name
df = get_all_cancer_features_from_one_folder(folder_path)
df['cancer_name'] = pd.Categorical(df['cancer_name'], CANCER_ORDER)
df = df.sort_values(by=['cancer_count'])
df.reset_index()
# print(df)

df = pd.merge(df, summary_df, left_on= 'cancer_name', right_on='cancer_desc')
df.drop(columns = 'cancer_desc', inplace = True)
# df = df[df['low2.5%'] != 0]
df = df.sort_values('cancer_count', axis=0, ascending=True)
df.reset_index(inplace= True, drop=True)
df = df[df["cancer_count"] >= 30] # choose these with enough sample size

with open(f'output/boot_HR/RA-original.pickle', 'rb') as handle:
    origin_HR_df = pickle.load(handle)

origin_HR_df.rename({'cancer_desc': 'cancer_name'}, inplace=True, axis=1)
df = pd.merge(df, origin_HR_df, on = ["cancer_name", "time_in_days"])
# %%
# make the plot
# import matplotlib 
# font = {'size'   : 20}

# matplotlib.rc('font', **font)
# matplotlib.rcParams.update({'font.size': 22})

N = len(df.cancer_name.unique())
ind = np.arange(N)
fig = plt.figure(figsize = (10,20))
ax = fig.add_subplot(111)
color_plate = sns.color_palette("husl", 7)
width = 0.15


for i, time in enumerate(df.time_in_days.unique()):
# for i, time in enumerate([1000]):
    df_tmp = df[df.time_in_days == time]
    # ax.barh(y_pos, performance, xerr=error, align='center')
    ax.barh(ind+width*i, width = df_tmp.hazard_ratio, height=width, color=color_plate[i],
        xerr=[df_tmp.hazard_ratio - df_tmp['low2.5%'], 
        df_tmp['hi97.5%'] - df_tmp.hazard_ratio],
        capsize=0, label=f"{time}-days")
    # ax.invert_xaxis()
    # df_tmp.plot.barh(x='cancer_name', y='HR',
    # xerr=[df_tmp.HR - df_tmp['low2.5%'], 
    #     df_tmp['hi97.5%'] - df_tmp.HR],capsize=0, width=0.2,
    # ax = ax)

plt.legend()
# ax.set_xticks(ind + width / 2, df.cancer_name.unique())
plt.yticks(ind + width / 2, df.cancer_name.unique())
max_height = 1 + np.nanmax(df['hi97.5%']) # ignore nan
# for i, v in enumerate(df['cancer_count']):
#     # print(i)
#     height = df['hi97.5%'].iloc[i]
#     ax.text(height + .03 * max_height, i-.25, str(v), color='blue', fontweight='bold')

plt.xlim(right = max_height - 0.6)
number, auto_name = split_number_and_name(subfolder_name)
df['auto_name'] = auto_name
df_list.append(df)
plt.axvline(x=1, color="black")
plt.title(f"{auto_name}")
ax.set_xlabel(f"Matched patient count = {number}")
create_dir('output/new_summary_fig')
# plt.savefig(f"output/new_summary_fig/time-{time}-RA_hazard_ratio_withCI.pdf", 
#     bbox_inches='tight') 
ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(20)
plt.xticks(fontsize= 20)
plt.yticks(fontsize= 20)
plt.legend(fontsize= 20)
ax.title.set_size(fontsize=20)
plt.savefig(f"output/new_summary_fig/RA_hazard_ratio_withCI.pdf", 
    bbox_inches='tight')  
plt.savefig(f"output/new_summary_fig/RA_hazard_ratio_withCI.png", dpi=200,
    bbox_inches='tight')    
# plt.savefig(f"../output/summary_fig/same_auto_different_cancer/{subfolder_name}.pdf", 
#     bbox_inches='tight')  


