'''
Plot HR as bars (default at 365 days)

move output_data/* from cloud to local first
'''
# %%
import pandas as pd
# from helper import get_survival_both
import numpy as np
from helper import cal_survival_risk 
from useful_chunk import create_dir
import matplotlib.pyplot as plt
import seaborn as sns
from plot_helper  import add_at_risk_counts
# %%
random_seed = 1234

def HR_CI_plot(plottype):
    '''
    Plot the HR for tons of cancers with CI bars

    Parameters
    ----------
    plottype : str
        can only be "all" or "focus"
        where "all" means investigate all cancertypes, annd "focus" means only work on important ones
    '''
    if plottype == 'all':
        cancer_list = ["all_cancers", "lip, oral cavity, and pharynx", "digestive organs", \
            "respiratory and intrathoracic organs", "bone and articular cartilage", \
            "skin", "soft tissue", "Kaposi's sarcoma", "breast", "female genital organs", \
            "male genital organs", "urinary tract", \
            "eye, brain and other parts of central nervous system", \
            "thyroid and other endocrine glands", \
            "ill-defined, other secondary and unspecified sites", \
            "neuroendocrine tumors", "lymphoid and hematopoietic tissue"]
    elif plottype == 'focus':
        cancer_list = [
            # "Malignant neoplasm of nasal cavities, middle ear and accessory sinuses", \
            'Malignant melanoma of skin',
            'Other and unspecified malignant neoplasm of skin',
            "Malignant neoplasm of larynx", \
            # "Malignant neoplasm of trachea, bronchus and lung", \
            # "Malignant neoplasm of trachea", \
            "Malignant neoplasm of main bronchus", \
            "Malignant neoplasm of lung and other parts of bronchus", \
            # "Malignant neoplasm of other and ill-defined sites within the respiratory system and intrathoracic organs", \
            # "Lymphosarcoma and reticulosarcoma", \
            "Hodgkin's disease", \
            "Other malignant neoplasms of lymphoid and histiocytic tissue", \
            "Multiple myeloma and immunoproliferative neoplasms", \
            "Lymphoid leukemia", \
            "Myeloid leukemia", \
            # "Other specified leukemia", \
            "Leukemia of unspecified cell type"]
    else:
        print("plottype should be either all or focus!")
        return 
    # merge all results in one df
    df_list = []
    for cancer_desc in cancer_list:
        ###
        df = pd.read_pickle(f'../output_data/boot_HR/RA-cancer_desc_{cancer_desc}-randomseed_{random_seed}.pickle')

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
        auto_risk_list = np.zeros(len(time_list))
        nonauto_risk_list = np.zeros(len(time_list))

        auto_risk_dict = cal_survival_risk(treat_survival_df, time_list)
        nonauto_risk_dict = cal_survival_risk(control_survival_df, time_list)
        for i, time in enumerate(time_list):
            auto_risk_list[i] = auto_risk_dict[time]
            nonauto_risk_list[i] = nonauto_risk_dict[time]
            HR_array[i] = np.round(
                float(auto_risk_dict[time]/nonauto_risk_dict[time]), 3)

        #                 cph = CoxPHFitter()
        # cph.fit(both_survival, duration_col='survivalTime', event_col='cancerFlag', 
        #     weights_col='weightN')
        # pvalue = cph.summary.loc['group', 'p']

        tmp_df = pd.DataFrame()
        tmp_df['hazard_ratio'] = HR_array
        tmp_df['time_in_days'] = time_list
        tmp_df['auto_risk'] = auto_risk_list
        tmp_df['nonauto_risk'] = nonauto_risk_list
        tmp_df['cancer_desc'] = cancer_desc
        tmp_df['cancer_count'] = treat_survival_df.cancerFlag.sum()

        df = df.merge(tmp_df, on=['cancer_desc', 'time_in_days'])
        df_list.append(df)

    # merge all the data
    df = pd.concat(df_list, axis=0)


    for label in ['upper', 'lower', 'hazard_ratio']:
        df[label] = np.round(df[label], 2)

    for label in ['auto_risk', 'nonauto_risk']:
        # df[label] = np.round(df[label] * 1e-6, 2)
        df[label] = np.round(df[label], 2)

    # lower_index = list(df.columns).index('lower')
    # upper_index = list(df.columns).index('upper')

    # df[['lower', 'upper']] = df[['upper', 'lower']] 
    # df.columns.values[lower_index] = 'upper'
    # df.columns.values[upper_index] = 'lower'

    df['expression'] = df.apply(lambda x: f"{x['hazard_ratio']}[{x['lower']}, {x['upper']}]", 
        axis = 1)

    # save the results
    if plottype == 'all':
        df.to_pickle('../output_data/all_HR_summary.pickle')
    elif plottype == 'focus':
        df.to_pickle('../output_data/focus_HR_summary.pickle')
    # df = pd.read_pickle('../output_data/HR_summary.pickle')

    df[df['time_in_days'] == 365].sort_values('cancer_count', ascending=False)

    # generate the report string
    df = df[df['time_in_days'] == 365].copy()
    df = df.sort_values('cancer_count', ascending=False)
    output = ""
    for i in range(len(df)):
        output += f"{df.iloc[i]['expression']} for the {df.iloc[i]['cancer_desc']} cancer; "

    # to excel
    df[df['time_in_days'] == 365].to_excel('../output/HR_summary_365.xlsx')

    df = df.sort_values('cancer_count', ascending=True)
    # N = len(df.cancer_desc.unique())
    color_plate = sns.color_palette("husl", 7)

    # df['cancer_desc'] = df[['cancer_desc', 'cancer_count']].apply(
    #     lambda row: "-".join([str(row['cancer_count']), row['cancer_desc']]), axis=1)
    df['cancer_desc'] = df[['cancer_desc', 'cancer_count']].apply(
        lambda row: f"{row['cancer_desc']} (n={row['cancer_count']})", axis=1)

    df = df[df['cancer_count'] > 20].copy()

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
    width = 1.0
    # ax.set_xticks(ind + width / 2, df.cancer_desc.unique())
    plt.yticks(ind, df.cancer_desc.unique())
    max_height = 1 + np.nanmax(df['upper']) # ignore nan

    plt.xlim(right = max_height - 0.6)
    df_list.append(df)
    plt.axvline(x=1, color="black")
    plt.title(f"RA, Matched patient count = {len(treat_survival_df)}")
    ax.set_xlabel(f"Hazard Ratio")
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

    # old
    # if plottype == "all":
    #     plt.savefig(f"../output/new_summary_fig/RA_hazard_ratio_withCI_time_{time}.png", dpi=600,
    #         bbox_inches='tight')   
    # elif plottype == "focus":
    #     plt.savefig(f"../output/new_summary_fig/RA_focus_hazard_ratio_withCI_time_{time}.png", dpi=600, 
    #         bbox_inches='tight')  

    # print version
    if plottype == "all":
        plt.savefig(f"../publish_figs/png/Figure2(a).png", dpi=600,
            bbox_inches='tight')   
        plt.savefig(f"../publish_figs/pdf/Figure2(a).pdf", dpi=600,
            bbox_inches='tight')   
    elif plottype == "focus":
        plt.savefig(f"../publish_figs/png/Figure2(b).png", dpi=600, 
            bbox_inches='tight')  
        plt.savefig(f"../publish_figs/pdf/Figure2(b).pdf", dpi=600, 
            bbox_inches='tight')  



# %%
if __name__ == "__main__":
    HR_CI_plot('all')
    HR_CI_plot('focus')
# %%
