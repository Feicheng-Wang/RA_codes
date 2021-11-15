# %%
import pandas as pd
from lifelines import KaplanMeierFitter

def kmf_plotter(data, label, ax=None, ci_show=True, plot_flag=True, loc_lower=None):
    
    '''
        data: need colnames survivalTime, cancerFlag and weightN
            e.g.
            cancerFlag	survivalTime	weightN
            0	False	72	1
            1	False	1771	1
            2	False	2198	1
            3	False	394	1
        label: usually have two types-- 'auto_group' and 'nonauto_group', only use in the legend
    ---
        return: survival plot and risk
    '''
    kmf = KaplanMeierFitter()
    T = data['survivalTime']
    E = data['cancerFlag']
    weights = data['weightN']
    kmf.fit(T, event_observed=E, weights=weights)
    if plot_flag is True:
        if loc_lower is None:
            if ci_show is True:
                loc_lower = 10
            else:
                loc_lower = 0
        if ax is None:
            ax = kmf.plot(label=label, loc=slice(loc_lower,4000), ci_show=ci_show)  
        else:
            ax = kmf.plot(label=label, ax=ax, loc=slice(loc_lower,4000), ci_show=ci_show)  
    cum_risk_500 = kmf.cumulative_density_at_times(times=500)
    cum_risk_1500 = kmf.cumulative_density_at_times(times=1500)
    cum_risk_3500 = kmf.cumulative_density_at_times(times=3500)
    return ax, cum_risk_500, cum_risk_1500, cum_risk_3500


def get_survival(df, cancer_icd_list, cancer_desc, mode):
    '''
    Get survival results of the treat/control group with one particular cancer as the event.
    Return
    ------
    Survival dataframe with three features survivalTime, weightN, cancerFlag.

    58 patients has Colo-rectum cancer
    cancerFlag  survivalTime  weightN
    0       False            72        1
    1       False          1771        1
    2       False          2198        1
    3       False           394        1
    4       False           974        1
    441 patients has Colo-rectum cancer
    cancerFlag  survivalTime   weightN
    0       False           597  0.004237
    1       False            51  0.004237
    2       False          2120  0.004237
    3       False           506  0.004237
    4       False           660  0.004237

    Parameters
    ----------
    df: df with cols cancerFlag, TreatCancerIcdShort, 
        AutoCancerDay, AutoLastEffectiveDay
        If mode = 'control' need 
            cancerFlag, ControlCancerIcdShort, 
            NonAutoCancerDay, NonAutoLastEffectiveDay,
            controlWeight
    cancer_icd_list: first 3 chars of the cancer icd in interest
        e.g. ['C17','C18','C19','C20']
    cancer_desc: the name of the cancer
    mode: can only be in 'treat' or 'control'
    '''
    assert mode in ['treat', 'control'], "mode should be treat or control!"
    Mode = mode.capitalize()
    AutoMode = 'Auto' if mode == 'treat' else 'NonAuto'
    # copy the treat_df
    func_df = df.copy()

    if len(cancer_icd_list) != 0:
        func_df['cancerFlag'] = func_df[f'{Mode}CancerIcdShort'].isin(cancer_icd_list)
    else:
        func_df['cancerFlag'] = ~func_df[f'{Mode}CancerIcdShort'].isna()
    num_cancer = func_df['cancerFlag'].sum()

    # show the number of cancers in that group
    print(f'In {mode} group, {num_cancer} patients has {cancer_desc} cancer')

    # if no cancer return None
    if num_cancer == 0:
        print(f"No cancer type = {cancer_desc}!")
        return None
    
    # change type if not Int64
    func_df[f'{AutoMode}CancerDay'] = func_df[f'{AutoMode}CancerDay'].astype('Int64')
    func_df[f'{AutoMode}LastEffectiveDay'] = func_df[f'{AutoMode}LastEffectiveDay'].astype('Int64')

    # AutoLastEffectiveDay cannot be smaller than AutoCancerDay
    assert (func_df[f'{AutoMode}LastEffectiveDay'] < func_df[f'{AutoMode}CancerDay']).sum() == 0, \
        'LastEffectiveDay before CancerDay!!!'
    
    survival_df = pd.DataFrame()
    survival_df['cancerFlag'] = func_df['cancerFlag']
    survival_df['survivalTime'] = func_df[f'{AutoMode}LastEffectiveDay']
    survival_df.loc[survival_df['cancerFlag'] == True, 'survivalTime'] = \
        func_df.loc[survival_df['cancerFlag'] == True, f'{AutoMode}CancerDay']

    # if control then need to copy weight from df
    if mode ==  'treat':
        survival_df['weightN'] = 1
    if mode == 'control':
        survival_df['weightN'] = func_df['controlWeight']

    assert all(survival_df['survivalTime'] >= 0), \
        "SurvivalTime should always be larger or equal to 0!!!"

    survival_df.reset_index(inplace=True, drop=True)

    if mode == 'control':
        weighted_num = (func_df['cancerFlag'] * func_df['controlWeight']).sum() 
        print(f'In weighted {mode} group, {weighted_num} patients has {cancer_desc} cancer')

    return survival_df

def get_survival_both(treat_df, control_df, cancer_icd_list, cancer_desc):
    '''
    Get survival results of both treat/control group with one particular cancer as the event.
    Return
    
    ------
    Survival dataframe with three features survivalTime, weightN, cancerFlag.

    58 patients has Colo-rectum cancer
    cancerFlag  survivalTime  weightN
    0       False            72        1
    1       False          1771        1
    2       False          2198        1
    3       False           394        1
    4       False           974        1
    441 patients has Colo-rectum cancer
    cancerFlag  survivalTime   weightN
    0       False           597  0.004237
    1       False            51  0.004237
    2       False          2120  0.004237
    3       False           506  0.004237
    4       False           660  0.004237

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        df with cols cancerFlag, TreatCancerIcdShort, 
        AutoCancerDay, AutoLastEffectiveDay
        If mode = 'control' need 
            cancerFlag, ControlCancerIcdShort, 
            NonAutoCancerDay, NonAutoLastEffectiveDay,
            controlWeight
    cancer_icd_list: list
        First 3 chars of the cancer icd in interest
        e.g. ['C17','C18','C19','C20']
    cancer_desc: str
        The name of the cancer
        e.g. 'Colo-rectum'
    mode: str
        Can only be 'treat' or 'control'

    Examples
    --------

    '''
    treat_survival_df = get_survival(treat_df, cancer_icd_list, cancer_desc, mode='treat')
    control_survival_df = get_survival(control_df, cancer_icd_list, 
        cancer_desc, mode='control')

    # sanity check the weight are same in two dataframes
    control_weight_sum = control_survival_df.weightN.sum()
    treat_weight_sum = treat_survival_df.weightN.sum()
    try:
        assert round(control_weight_sum - treat_weight_sum, 4) == 0, 'Weight sum in treat and control group are not equal!!'
    except AssertionError as err:
        print("AssertionError: {0}".format(err))
        print(f"ControlWeightSum: {control_weight_sum}")
        print(f"TreatWeightSum: {treat_weight_sum}")
        print(f"Difference: {round(control_weight_sum - treat_weight_sum, 4)}")
        raise
    
    return treat_survival_df, control_survival_df


def cal_survival_risk(data, times=[10, 30, 90, 180, 365, 1000]):
    '''
        data: need colnames survivalTime, cancerFlag and weightN
        times: several times to calculate the cumulative survival risk
    ---
        return: a risk_dict with 
            key: 10, 30... and 
            value: the cumulative survival risk
    '''
    kmf = KaplanMeierFitter()
    T = data['survivalTime']
    E = data['cancerFlag']
    weights = data['weightN']
    kmf.fit(T, event_observed=E, weights=weights)
    risk_dict = {}
    for time in times:
        risk_dict[time] = kmf.cumulative_density_at_times(times=time)
    return risk_dict


def produce_survival_result_treat(data, auto_type, cancer_desc):
    # create_dir(f'output/treat_survival_data/{auto_type}')
    # only consider those started with selected auto_type (e.g. 'Rheumatoid arthritis')
    if auto_type is None:
        treat_one_auto_type = data.copy()
    else:
        treat_one_auto_type = data[data['PheWASString'] == auto_type]

    if cancer_desc is None:
        treat_one_auto_type['cancerFlag'] = pd.notna(treat_one_auto_type['description'])
    else:
        treat_one_auto_type['cancerFlag'] = (treat_one_auto_type['description'] == 
            cancer_desc)
    # treat_one_auto_type

    # survival time and weight
    treat_one_auto_type_event = treat_one_auto_type[
        treat_one_auto_type['cancerFlag'] == True]



    if len(treat_one_auto_type_event.index) == 0:
        print(f"No cancer type = {cancer_desc}!")
    else:
        treat_one_auto_type_event['AutoCancerDay'] = \
            treat_one_auto_type_event['AutoCancerDay'].apply(int)
        # treat_event = treat_one_auto_type_event['AutoCancerDay'].value_counts()
        survival_df_event = pd.DataFrame()
        survival_df_event['survivalTime'] = treat_one_auto_type_event['AutoCancerDay']
        # survival_df_event['weightN'] = treat_event.values
        survival_df_event['weightN'] = 1
        survival_df_event['cancerFlag'] = 1

        treat_one_auto_type_noevent = \
            treat_one_auto_type[treat_one_auto_type['cancerFlag'] == False]
        treat_one_auto_type_noevent['AutoLastEffectiveDay'] = \
            treat_one_auto_type_noevent['AutoLastEffectiveDay'].apply(int)
        # treat_noevent = treat_one_auto_type_noevent['AutoLastEffectiveDay'].value_counts()
        survival_df_noevent = pd.DataFrame()
        # survival_df_noevent['survivalTime'] = treat_noevent.index
        survival_df_noevent['survivalTime'] = \
            treat_one_auto_type_noevent['AutoLastEffectiveDay']
        survival_df_noevent['weightN'] = 1
        survival_df_noevent['cancerFlag'] = 0

        survival_df = pd.concat([survival_df_event, survival_df_noevent], axis=0)

        if not all(survival_df['survivalTime'] >= 0):
            print("SurvivalTime should always be larger or equal to 0!!!")
            return None
            # exit()
        
        # survival_df = survival_df[survival_df['survivalTime'] > 0]
        # print(survival_df)

        # with open(f'output/treat_survival_data/{auto_type}/{cancer_desc}.pkl', 'wb') as f:
        #     pickle.dump(survival_df, f) 
        return survival_df


def produce_survival_result_control(data, cancer_desc):
    # create_dir(f'output/control_survival_data/{auto_type}')
    '''
        only reform those who has descriptions
    '''
    control_one_auto_type = data.copy()
    if cancer_desc is None:
        control_one_auto_type['cancerFlag'] = pd.notna(control_one_auto_type['description'])
    else:
        control_one_auto_type['cancerFlag'] = control_one_auto_type['description'] == cancer_desc
    # control_one_auto_type

    # survival time and weight
    control_one_auto_type_event = control_one_auto_type[control_one_auto_type['cancerFlag'] == True]


    if len(control_one_auto_type_event.index) == 0:
        print(f"No cancer type = {cancer_desc}!")
        return None
    else:
        control_one_auto_type_event['NonAutoCancerDay'] = control_one_auto_type_event['NonAutoCancerDay'].apply(int)
        # survival_df_event = control_one_auto_type_event[['NonAutoCancerDay', 'controlWeight']].groupby(
        #     ['NonAutoCancerDay'])['controlWeight'].sum().reset_index(name ='weightN')
        # survival_df_event.columns = ['survivalTime', 'weightN']
        survival_df_event = pd.DataFrame()
        survival_df_event['survivalTime'] = control_one_auto_type_event['NonAutoCancerDay']
        survival_df_event['weightN'] = control_one_auto_type_event['controlWeight']
        survival_df_event['cancerFlag'] = 1

        control_one_auto_type_noevent = \
            control_one_auto_type[control_one_auto_type['cancerFlag'] == False]
        # survival_df_noevent = control_one_auto_type_noevent[['NonAutoLastEffectiveDay', 'controlWeight']].groupby(
        #     ['NonAutoLastEffectiveDay'])['controlWeight'].sum().reset_index(name ='weightN')
        # survival_df_noevent.columns = ['survivalTime', 'weightN']
        survival_df_noevent = pd.DataFrame()
        survival_df_noevent['survivalTime'] = control_one_auto_type_noevent['NonAutoLastEffectiveDay']
        survival_df_noevent['weightN'] = control_one_auto_type_noevent['controlWeight']
        survival_df_noevent['cancerFlag'] = 0

        survival_df = pd.concat([survival_df_event, survival_df_noevent], axis=0)
        survival_df = survival_df.dropna()

        #sanity check
        if not all(survival_df['survivalTime'] > 0):
            print("SurvivalTime should always be larger or equal to 0!!!")
            exit()
        # survival_df = survival_df[survival_df['survivalTime'] > 0]
        # print(survival_df)

        # with open(f'output/control_survival_data/{auto_type}/{cancer_desc}.pkl', 'wb') as f:
        #     pickle.dump(survival_df, f) 
        
        return survival_df
