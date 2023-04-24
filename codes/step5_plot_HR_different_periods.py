# %%
import pandas as pd
# from helper import get_survival_both
import numpy as np
from helper import cal_survival_risk 
from useful_chunk import create_dir
import matplotlib.pyplot as plt
import seaborn as sns
from plot_helper  import add_at_risk_counts, remove_spines
from helper import kmf_plotter
import pickle
sns.set_style("darkgrid")

# %%
og_df = pd.read_pickle('../output_data/all_HR_summary.pickle')
df = og_df[og_df.time_in_days != 10].copy()
df = df[df.cancer_count >= 200].copy() 
# %%
df['Days'] = df['time_in_days']
df['Hazard Ratio'] = df['hazard_ratio']
df.loc[df['cancer_desc'] == 'all_cancers', 'cancer_desc'] = 'all cancers'
# sns.set(rc = {'figure.figsize':(15,8)}, font_scale=1.2)
# g = sns.FacetGrid(df, col="cancer_desc", col_wrap=4)
# g.map(sns.lineplot, "Days", 'Hazard Ratio')
# g.set_titles(col_template="{col_name}", row_template="{row_name}")
# for cancer_desc, ax in g.axes_dict.items():
#     tmp_df = df[df['cancer_desc'] == cancer_desc]
#     ax.fill_between(tmp_df.time_in_days, tmp_df.lower, tmp_df.upper, alpha=0.3)
#     ax.axhline(1, color='black')
#     ax.text(0.5,-0.5, "(a) my label", size=12, ha="center", 
#          transform=ax.transAxes)

# for axis in g.axes.flat:
#     axis.tick_params(labelleft=True, labelbottom=True)

# # g.tight_layout()
# g.fig.subplots_adjust(top=0.8) # adjust the Figure in rp
# g.fig.suptitle('Hazard ratio across time with different cancer types')

# # g.savefig('../output/HR_across_time_new.pdf')
# g.savefig('../output/HR_across_time_new.png', dpi=300)

n_row = 3
n_col = 3
sns.set(rc = {'figure.figsize':(8 * n_col,8 * n_row)}, font_scale=2)
fig, axs = plt.subplots(n_row, n_col, sharex=True, sharey=True)
CANCER_NAMES = df.cancer_desc.unique()

for i in range(len(CANCER_NAMES)):
# for cancer_desc, ax in g.axes_dict.items():
    ax = axs[i // n_col, i % n_col]
    cancer_desc = CANCER_NAMES[i]
    tmp_df = df[df['cancer_desc'] == cancer_desc].copy()
    ax.plot(tmp_df.time_in_days, tmp_df.hazard_ratio)
    ax.yaxis.set_tick_params(labelleft=True) # show yaxis ticks
    ax.xaxis.set_tick_params(labelbottom=True) # show yaxis ticks
    ax.set_xticks([0, 500, 1000])
    ax.set_xlabel('Days')
    ax.set_ylabel('Hazard Ratio')
    ax.set_title(cancer_desc)
    ax.fill_between(tmp_df.time_in_days, tmp_df.lower, tmp_df.upper, alpha=0.3)
    ax.axhline(1, color='black')
    # print(ax.get_xticks())

    ## add count
    if cancer_desc == "all cancers":
        cancer_desc = "all_cancers"
    with open(f'../output_data/survival_analysis/{cancer_desc}.pickle', 'rb') as f:
        cancer_icd_list, cancer_desc, treat_survival_df, control_survival_df = \
            pickle.load(f)

    kmf_treat, _, treat_risk_at500, treat_risk_at1500, treat_risk_at3500 = \
        kmf_plotter(data = treat_survival_df, label='RA patients', return_kmf=True,
        plot_flag=False)
    kmf_control, _, control_risk_at500, control_risk_at1500, control_risk_at3500 = \
        kmf_plotter(data = control_survival_df, label='non RA patients', return_kmf=True,
        plot_flag=False)
    add_at_risk_counts(kmf_treat, kmf_control, ax=ax, xticks=[0, 500, 1000], label_head=(i % n_col == 0),
        ypos=-0.5 - 0.1 * (i // n_col))

# remove_spines(axs[-1,-1], ["top", "right", "bottom", "left"])
fig.delaxes(axs[-1][-1])
fig.delaxes(axs[-1][-2])
fig.suptitle('Hazard ratio across time with different cancer types')
fig.tight_layout()


## to add patient at risk data
# fig.savefig('../output/HR_across_time.pdf', bbox_inches='tight')
fig.savefig(f"../publish_figs/png/FigureS1.png", dpi=600, 
    bbox_inches='tight')  
fig.savefig(f"../publish_figs/pdf/FigureS1.pdf", dpi=600, 
    bbox_inches='tight')  
# %%
CANCER_NAMES = ["all cancers", 
    "respiratory and intrathoracic organs", "skin", "lymphoid and hematopoietic tissue"]
df = df[df['cancer_desc'].isin(CANCER_NAMES)].copy()

sns.set(rc = {'figure.figsize':(16,16)}, font_scale=1.8)
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)

for i in range(len(CANCER_NAMES)):
# for cancer_desc, ax in g.axes_dict.items():
    ax = axs[i // 2, i % 2]
    cancer_desc = CANCER_NAMES[i]
    tmp_df = df[df['cancer_desc'] == cancer_desc].copy()
    ax.plot(tmp_df.time_in_days, tmp_df.hazard_ratio)
    ax.yaxis.set_tick_params(labelleft=True) # show yaxis ticks
    ax.xaxis.set_tick_params(labelbottom=True) # show yaxis ticks
    ax.set_xticks([0, 500, 1000])
    ax.set_xlabel('Days')
    ax.set_ylabel('Hazard Ratio')
    ax.set_title(cancer_desc)
    ax.fill_between(tmp_df.time_in_days, tmp_df.lower, tmp_df.upper, alpha=0.3)
    ax.axhline(1, color='black')
    # print(ax.get_xticks())

    ## add count
    if cancer_desc == "all cancers":
        cancer_desc = "all_cancers"
    with open(f'../output_data/survival_analysis/{cancer_desc}.pickle', 'rb') as f:
        cancer_icd_list, cancer_desc, treat_survival_df, control_survival_df = \
            pickle.load(f)

    kmf_treat, _, treat_risk_at500, treat_risk_at1500, treat_risk_at3500 = \
        kmf_plotter(data = treat_survival_df, label='RA patients', return_kmf=True,
        plot_flag=False)
    kmf_control, _, control_risk_at500, control_risk_at1500, control_risk_at3500 = \
        kmf_plotter(data = control_survival_df, label='non RA patients', return_kmf=True,
        plot_flag=False)
    add_at_risk_counts(kmf_treat, kmf_control, ax=ax, xticks=[0, 500, 1000], label_head=(i % 2 == 0),
        ypos=-0.6 - 0.8 * (i // 2))


 
fig.suptitle('Hazard ratio across time with different cancer types')
fig.tight_layout()

## to add patient at risk data
# fig.savefig('../output/HR_across_time_short.pdf', bbox_inches='tight')
fig.savefig(f"../publish_figs/png/Figure3.png", dpi=600, 
    bbox_inches='tight')  
fig.savefig(f"../publish_figs/pdf/Figure3.pdf", dpi=600, 
    bbox_inches='tight')  
# %%

# %%
kmf_treat