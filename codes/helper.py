# %%
import pandas as pd

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

    func_df['cancerFlag'] = func_df[f'{Mode}CancerIcdShort'].isin(cancer_icd_list)
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
