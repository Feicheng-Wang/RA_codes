# %%
import pandas as pd
import numpy as np
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

    # merge on 
    # treat_df: 'FirstServiceAuto', 'FirstAutoIcd
    # control_df: 'AutoFirstServiceAuto', 'TreatGroupFirstAutoIcd'
    treat_df = treat_df[['MemberId', 'FirstServiceAuto', 'FirstAutoIcd']]
    treat_df.columns = ['AutoMemberId', 'FirstServiceAuto', 'FirstAutoIcd']
    treat_df['FirstServiceAuto'] = treat_df['FirstServiceAuto'].astype(str)
    control_df = control_df[
        ['NonAutoMemberId', 'AutoFirstServiceAuto', 'TreatGroupFirstAutoIcd']]
    control_df.sort_values('NonAutoMemberId', inplace=True)
    control_df.columns = ['NonAutoMemberId', 'FirstServiceAuto', 'FirstAutoIcd']

    df = pd.merge(control_df, treat_df, on=['FirstServiceAuto', 'FirstAutoIcd'],
                  how='left')
    df.set_index('NonAutoMemberId', inplace=True)
    df['Weight'] = df.groupby(pd.Grouper(level=0, sort='sorted'))[
        'FirstAutoIcd'].transform(lambda x: 1/len(x))
    control_treat_w = df.groupby('AutoMemberId')['Weight'].sum()

    # save result
    control_treat_w.to_pickle('../data/control_treat_w.pkl')
# df.groupby('NonAutoMemberId').apply(lambda x: x.sample(n=1)).reset_index(drop=True)
# %%


# %%
df.iloc[:10000].groupby(pd.Grouper(level=0, sort='sorted'))[
    'FirstAutoIcd'].transform(lambda x: 1/len(x))
# %%

# %%
