# %%
import pandas as pd
import numpy as np

'''
treat_df: RA_member_summary.p
drug_df: RA_member_summary_with_drug_full_cover_auto.xls

treat: N = 68415
drug: N = 32847

Sex N %
F
M

Age
[0, 40)
[40, 50)
[50, 60)
[60, 70)
[70, 80)
[80, 120)

AVGIncome
AVGDiagRate
AVGVisitRate

'''

def summarize_feature(df, colname, cut=None, total_N=None, random_state=42,
                      index_name=None):
    np.random.seed(random_state)
    df = df.copy()
    if total_N is None:
        total_N = len(df)
    if cut is not None:
        df[colname + '_group'] = pd.cut(df[colname], cut, right=False)
        colname = colname + '_group'
    if 'w' not in df.columns:
        df['w'] = 1
    summary_df = pd.DataFrame()
    og_N = df.groupby(colname)['w'].sum().sort_index()
    percent_ = og_N / og_N.sum() * 100

    # distribution of original population
    summary_df['og_N'] = og_N
    summary_df['og_percent'] = np.round(percent_, 2)

    # find the sample size for target population
    N_ = np.floor(total_N * percent_/100)
    resid_N = total_N - np.sum(N_)

    # randomly sample to compensate the difference in sample size
    sample = np.random.choice(np.arange(0, len(og_N)), size=int(resid_N), 
                              replace=False)
    N_[sample] += 1

    # summarize the target population 
    # and diff in percent to original population
    summary_df['N'] = N_.astype(int)
    summary_df['percent'] = np.round(
        summary_df['N'] / summary_df['N'].sum() * 100, 2)
    summary_df['percent_diff'] = \
        summary_df['percent'] - summary_df['og_percent']

    print(summary_df)

    # only keep required output
    summary_df = summary_df[['N', 'percent']]
    summary_df['N'] = summary_df['N'].apply(
        lambda x: str(x)[:-3] + ',' + str(x)[-3:] \
            if len(str(x)) > 3 else str(x))

    # create a new level of index
    if index_name is None:
        index_name = colname
    new_index = pd.MultiIndex.from_arrays(
        [[index_name] * len(summary_df), summary_df.index])

    # set the new index to the Series
    summary_df.index = new_index
    summary_df.columns = ['N', '%']
    return summary_df
    
def patient_characteristics(df, total_N=None):
    df_list = []
    df['All'] = 1
    tmp_df = summarize_feature(df, 'All', total_N=total_N,
                                     index_name='All')
    tmp_df.index = pd.MultiIndex.from_arrays([['All'], ['']])
    df_list.append(tmp_df)
    df_list.append(summarize_feature(df, 'Gender', total_N=total_N,
                                     index_name='Gender'))
    df_list.append(summarize_feature(df, 'age_at_RA', 
                                     cut=[0, 40, 50, 60, 70, 80, 120], 
                                     total_N=total_N,
                                     index_name='Age at RA diagnosis'))
    df_list.append(summarize_feature(df, 'AVGIncome', total_N=total_N, 
                      cut=[0, 35000, 50000, 70000, 100000, 500000],
                      index_name='Average income'))
    df_list.append(summarize_feature(df, 'AVGDiagRate', total_N=total_N, 
                      cut=[0, 0.03, 0.1, 0.3, 1, np.infty],
                      index_name='Average diagnosis rate'))
    df_list.append(summarize_feature(df, 'AVGVisitRate', total_N=total_N, 
                      cut=[0, 0.01, 0.02, 0.05, 0.1, np.infty],
                      index_name='Average visit rate'))
    df = pd.concat(df_list, axis=0)
    return df


# %%
if __name__ == "__main__":
    # read data
    treat_df = pd.read_pickle('../data/RA_member_summary.p')
    treat_w_df = pd.read_pickle('../data/treat_data_RA.pkl')
    control_df = pd.read_pickle('../data/control_data_RA.pkl')
    treat_df['AutoMemberId'] = treat_df['MemberId'].apply(
        lambda x: x.zfill(20))
    treat_df = treat_df[treat_df['AutoMemberId'].isin(
        treat_w_df['AutoMemberId'])].copy()
    control_treat_w = pd.read_pickle('../data/control_treat_w.pkl')
    
    drug_df = pd.read_excel(
        "../data/RA_member_summary_with_drug_full_cover_auto.xls")
    drug_df['age_at_RA'] = (drug_df.FirstServiceAuto.apply(
        lambda x: int(x[:4])) - drug_df.BirthYear)
    drug_df.dropna(subset=['age_at_RA'], inplace=True)
    drug_df['age_at_RA'] = drug_df['age_at_RA'].astype(int)
    
    summary_treat = patient_characteristics(treat_df, total_N=68415)
    summary_treat.columns = pd.MultiIndex.from_arrays(
        [['Matched RA patients'] * len(summary_treat.columns), 
         summary_treat.columns]
    )
    summary_drug = patient_characteristics(drug_df, total_N=32847)
    summary_drug.columns = pd.MultiIndex.from_arrays(
        [['RA patients with medication presciption'] * len(summary_drug.columns), 
         summary_drug.columns]
    )
    treat_df_w = treat_df.merge(control_treat_w.to_frame(name='w'), 
                   left_on=['MemberId'], right_index=True)
    treat_df_w.loc[treat_df['Gender'] == 'M', 'w'] *= 1

    summary_treat_w = patient_characteristics(treat_df_w, total_N=1340538)
    summary_drug.columns = pd.MultiIndex.from_arrays(
        [['Matched non-RA patients'] * len(summary_treat_w.columns), 
         summary_treat_w.columns]
    )
    df = pd.concat([summary_treat, summary_drug, summary_treat_w], axis=1)

    # create a new MultiIndex with int dtype
    df.index =  pd.MultiIndex.from_arrays(
        [df.index.get_level_values(0).astype(str), 
         df.index.get_level_values(1).astype(str)], 
         names=df.index.names)
    print(df)

    # Save DataFrame to an Excel file
    file_name = 'notes/output.xlsx'
    df.to_excel(file_name, index=True, engine='openpyxl')


# %%
def foo(a):
    return 1/2 * a + 1/2 * a ** 3.3

print(foo(0.91656) - 5/6)
# %%
a = 0.91656
(1 - a ** 3.3) / (1 - a)
# 1-p = 0.91
# p = 0.09
# %%
