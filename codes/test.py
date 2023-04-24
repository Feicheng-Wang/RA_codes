'''
plot survival plot for most important cancers
'''
# %%
import pandas as pd
import pickle
from helper import kmf_plotter
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
import numpy as np
from useful_chunk import create_dir
# from lifelines.plotting import add_at_risk_counts
# from plot_helper import remove_spines, move_spines, remove_ticks, is_latex_enabled
from plot_helper import add_at_risk_counts


# read data
# treat_df = pd.read_pickle('../data/treat_data_RA.pkl')
# control_df = pd.read_pickle('../data/control_data_RA.pkl')

# %%
'''
"lymphoid and hematopoietic tissue"
"respiratory and intrathoracic organs"
"Malignant neoplasm of trachea, bronchus and lung"
"Multiple myeloma and immunoproliferative neoplasms"
"Other malignant neoplasms of lymphoid and histiocytic tissue"
"Other and unspecified malignant neoplasm of skin"
'''
plt.rcParams.update({'font.size': 15})

def survival_plot_one_cancer(cancer_desc, image_type='png'):
    '''
    Plot the survival curve for comparing RA and non-RA patients on one specific cancer.
    
    Parameters
    ----------
    cancer_desc: str
        e.g. "lymphoid and hematopoietic tissue", "respiratory and intrathoracic organs"
    '''
    with open(f'../output_data/survival_analysis/{cancer_desc}.pickle', 'rb') as f:
        cancer_icd_list, cancer_desc, treat_survival_df, control_survival_df = \
            pickle.load(f)

    fig, ax = plt.subplots(figsize=(12, 4))
    kmf_treat, ax, treat_risk_at500, treat_risk_at1500, treat_risk_at3500 = \
        kmf_plotter(data = treat_survival_df, label='RA patients', return_kmf=True)
    kmf_control, ax, control_risk_at500, control_risk_at1500, control_risk_at3500 = \
        kmf_plotter(data = control_survival_df, label='non RA patients', ax=ax, return_kmf=True)


    '''
    calculate the log rank test p value
    actually here is the weighted version, 
    so we use the cox proportional hazard model to do the test
    marking treatment as group 1, control as group 2, and test whether or not p < 0.05
    '''
    nonauto_survival_short = control_survival_df[['survivalTime', 
        'weightN', 'cancerFlag']].groupby(
        ['survivalTime', 'cancerFlag'])['weightN'].sum().reset_index(name ='weightN')

    auto_survival_short = treat_survival_df[['survivalTime', 
        'weightN', 'cancerFlag']].groupby(
        ['survivalTime', 'cancerFlag'])['weightN'].sum().reset_index(name ='weightN')

    auto_survival_short['group'] = 1
    nonauto_survival_short['group'] = 0
    both_survival = pd.concat([auto_survival_short, nonauto_survival_short], axis=0)

    cph = CoxPHFitter()
    cph.fit(both_survival, duration_col='survivalTime', event_col='cancerFlag', 
        weights_col='weightN')
    pvalue = cph.summary.loc['group', 'p']
    if pvalue < 1e-4:
        text = "p < 1e-4"
    else:
        text = f"p = {np.round(pvalue, 4)}"

    # save the plot
    hazard_at_1500 = np.round(float(treat_risk_at1500/control_risk_at1500), 3)
    cancer_count = treat_survival_df.loc[treat_survival_df['cancerFlag'] == 1, 'weightN'].sum()

    # create the folder needed to hold the results
    create_dir('../output/survival_plots')
    base_path = f'../output/survival_plots/{cancer_desc}'
    create_dir(base_path)

    ax.set_xlim(left = -200, right=4000)
    ax.set_title(f'\
    RA vs non-RA patient survival plot on {cancer_desc} cancer\n'
    f'Hazard ratio at day 1500 = {hazard_at_1500}\n'
    f'RA group cancer patient counts = {cancer_count}')
    plt.xlabel("Days")
    
    ax, ticklabels = add_at_risk_counts(kmf_treat, kmf_control, ax=ax)

    plt.tight_layout()

    if pvalue < 1e-4:
        ax.text(0.05, 0.05, text, c='red', transform=ax.transAxes)
    else:
        ax.text(0.05, 0.05, text, transform=ax.transAxes)

    if image_type == 'png':
        plt.savefig(f'{base_path}/cancer_count={cancer_count}-hazard={hazard_at_1500}-{cancer_desc}.png', dpi=200)
    else:
        plt.savefig(f'{base_path}/cancer_count={cancer_count}-hazard={hazard_at_1500}-{cancer_desc}.pdf')

    return kmf_treat, kmf_control, ticklabels
# # %%
# survival_plot_one_cancer("lymphoid and hematopoietic tissue")
# # %%
# survival_plot_one_cancer("respiratory and intrathoracic organs")
kmf_treat, kmf_control, ticklabels = survival_plot_one_cancer("lymphoid and hematopoietic tissue")
plt.tight_layout()
# %%
ax = plt.gca()
ax.set_xticklabels(ticklabels, ha="right") # horizontalalignment
# %%
f = kmf_control
tick = 500.0
event_table_slice = (
    f.event_table.assign(at_risk=lambda x: x.at_risk - x.removed)
    .loc[:tick, ["at_risk", "censored", "observed"]]
    .agg({"at_risk": "min", "censored": "sum", "observed": "sum"})
    .rename({"at_risk": "At risk", "censored": "Censored", "observed": "Events"})
)
event_table_slice
# %%
import seaborn as sns

sns.set(style="ticks")
sns.set_style("darkgrid")
sns.set(font_scale=1.5)

### China Gini illustation
value = np.array([0, 500, 1000, 2000, 5000, 10000, 1e5, 5e5, 1e6, 1e7])
population = np.array([0, 5.6, 3.1, 3.8, 0.8, 0.4, 0.25, 0.05, 0.01, 0.001])

## calculation
total_gdp = np.sum(value * population)
print(total_gdp)
total_population = np.sum(population)
print(total_population)

cumsum_gdp = np.cumsum(value * population)
print(cumsum_gdp)

cumsum_population = np.cumsum(population)

## calculate GINI coef 
full_area = total_gdp * total_population / 2
area_under_red = 0
for i in range(len(cumsum_population) - 1): 
    area_under_red += population[i+1] * (cumsum_gdp[i] + cumsum_gdp[i+1]) / 2
gini = 1 - np.round(area_under_red / full_area, 2)
print(gini)

## make plot
fig = plt.figure(figsize = (10,10))
plt.plot(cumsum_population, cumsum_gdp, color='red', label='??')
slope = cumsum_gdp[-1] / cumsum_population[-1]
optimal_line = cumsum_population * slope
plt.plot(cumsum_population, optimal_line, color='green', label='ideal')
plt.axhline(0, color='black')
plt.axvline(cumsum_population[-1], color='black')

plt.fill_between(cumsum_population, cumsum_gdp, optimal_line, color='grey', alpha=0.5)
# plt.xlabel("Population (100 million)")
# plt.ylabel("Cumulative Income (100 million yuan)")
# plt.title("Gini coef = ")
plt.legend()

# %%
