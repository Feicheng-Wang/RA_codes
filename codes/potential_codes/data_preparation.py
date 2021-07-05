# %%
import pandas as pd
# %% 
'''
AutoMemberId	AutoFirstServiceAuto	AutoCancerDay	AutoLastEffectiveDay	TreatGroupFirstAutoIcd	TreatGroupFirstCancerIcd	PheWASString	TreatCancerIcdShort	description
0	00000022636945834925	2008-11-11	463.0	2210.0	340	174.9	Multiple sclerosis	174	NaN
1	00000008092902351825	2013-04-17	NaN	2235.0	340	NaN	Multiple sclerosis	nan	NaN
2	00231512182229022101	2014-11-19	NaN	1868.0	340	NaN	Multiple sclerosis	nan	NaN
3	00121216131824131101	2012-08-13	1348.0	2696.0	340	C49.4	Multiple sclerosis	C49	NaN
4	00000014239430081325	2013-10-28	NaN	2255.0	340	NaN	Multiple sclerosis	nan	NaN
'''
treat_df = pd.read_pickle('../../data/treat_data_RA.pkl')

# treat_df = pd.read_csv('data/treat_data_RA.pkl')
# %%
'''
NonAutoMemberId	AutoFirstServiceAuto	ControlStartDay	NonAutoCancerDate	NonAutoLastEffectiveDate	TreatGroupFirstAutoIcd	ControlGroupFirstCancerIcd	controlWeight	NonAutoCancerDay	NonAutoLastEffectiveDay	PheWASString	ControlCancerIcdShort	description
0	00121223350002341201	2010-03-11	2009-11-10	NaN	2011-06-30	714.0	NaN	0.004237	NaN	597	Rheumatoid arthritis	nan	NaN
1	00121226120736261101	2010-03-11	2009-11-10	NaN	2009-12-31	714.0	NaN	0.004237	NaN	51	Rheumatoid arthritis	nan	NaN
2	00121226060102271101	2010-03-11	2009-11-10	NaN	2015-08-31	714.0	NaN	0.004237	NaN	2120	Rheumatoid arthritis	nan	NaN
3	00000018693746595125	2010-03-11	2009-11-10	NaN	2011-03-31	714.0	NaN	0.004237	NaN	506	Rheumatoid arthritis	nan	NaN
4	00000007290661887525	2010-03-11	2010-03-11	NaN	2011-12-31	714.0	NaN	0.004237	NaN	660	Rheumatoid arthritis	nan	NaN
'''
control_df = pd.read_pickle('../../data/control_data_RA.pkl')

# %%
'''
'''
treat_df = pd.read_pickle('../../data/treat_data_final.pkl')

# %%
treat_df = treat_df[treat_df['PheWASString'] == 'Rheumatoid arthritis']
# %%
'''
Change the type of each column of treat_df
    AutoMemberId to string with length 20 fill in leading zeros
        e.g. 00231813342900020001
    AutoCancerDay and AutoLastEffectiveDay to Int64
    
'''
treat_df['AutoMemberId'] = treat_df['AutoMemberId'].apply(lambda x: str(x).zfill(20))
treat_df['AutoCancerDay'] = treat_df['AutoCancerDay'].astype('Int64')
treat_df['AutoLastEffectiveDay'] = treat_df['AutoLastEffectiveDay'].astype('Int64')
# %%
treat_df.to_pickle('../../data/treat_data_RA.pkl')
# %%
'''
Change the type of each column of control_df

'''
control_df['NonAutoCancerDay'] = control_df['NonAutoCancerDay'].astype('Int64')
# %%
control_df.to_pickle('../../data/control_data_RA.pkl')
# %%
