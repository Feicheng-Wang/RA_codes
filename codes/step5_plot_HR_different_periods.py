# %%
import pandas as pd
# from helper import get_survival_both
import numpy as np
from helper import cal_survival_risk 
from useful_chunk import create_dir
import matplotlib.pyplot as plt
import seaborn as sns

og_df = pd.read_pickle('../output_data/HR_summary.pickle')
# %%
df = og_df[og_df.time_in_days != 10].copy()
df = df[df.cancer_count >= 200].copy() 
# %%
sns.set(rc = {'figure.figsize':(15,8)}, font_scale=1.2)
g = sns.FacetGrid(df, col="cancer_desc", col_wrap=4)
g.map(sns.lineplot, "time_in_days", 'hazard_ratio')
g.set_titles(col_template="{col_name}", row_template="{row_name}")
for cancer_desc, ax in g.axes_dict.items():
    tmp_df = df[df['cancer_desc'] == cancer_desc]
    ax.fill_between(tmp_df.time_in_days, tmp_df.lower, tmp_df.upper, alpha=0.3)
    ax.axhline(1, color='black')

for axis in g.axes.flat:
    axis.tick_params(labelleft=True, labelbottom=True)

g.tight_layout()
g.fig.subplots_adjust(top=0.9) # adjust the Figure in rp
g.fig.suptitle('Hazard ratio across time with different cancer types')

g.savefig('../output/HR_across_time.pdf')
# %%
