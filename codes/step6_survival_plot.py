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

    fig, ax = plt.subplots(figsize=(12, 6))
    ax, treat_risk_at500, treat_risk_at1500, treat_risk_at3500 = kmf_plotter(
        data = treat_survival_df, label='RA patients')
    ax, control_risk_at500, control_risk_at1500, control_risk_at3500 = kmf_plotter(
        data = control_survival_df, label='non RA patients', ax=ax)


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

    if pvalue < 1e-4:
        ax.text(0.05, 0.05, text, c='red', transform=ax.transAxes)
    else:
        ax.text(0.05, 0.05, text, transform=ax.transAxes)

    if image_type == 'png':
        fig.savefig(f'{base_path}/cancer_count={cancer_count}-hazard={hazard_at_1500}-{cancer_desc}.png', dpi=200)
    else:
        fig.savefig(f'{base_path}/cancer_count={cancer_count}-hazard={hazard_at_1500}-{cancer_desc}.pdf')

# # %%
# survival_plot_one_cancer("lymphoid and hematopoietic tissue")
# # %%
# survival_plot_one_cancer("respiratory and intrathoracic organs")
# %%
cancer_list = [
"lymphoid and hematopoietic tissue",
"respiratory and intrathoracic organs",
"Malignant neoplasm of trachea, bronchus and lung",
"Multiple myeloma and immunoproliferative neoplasms",
"Other malignant neoplasms of lymphoid and histiocytic tissue",
"Other and unspecified malignant neoplasm of skin",]
for cancer in cancer_list:
    survival_plot_one_cancer(cancer)
# %%
