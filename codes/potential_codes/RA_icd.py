# %%
import pandas as pd

# %%
df = pd.read_csv('/Users/feichengwang/gitbase/Research/Sam/RA_codes/data/auto_icd.csv')
df
# %%
df[df['PheWASString'] == 'Rheumatoid arthritis'].sort_values('icd')[
    ['icd', 'PheWASCode', 'PheWASString', 'DESumls']].to_csv(
        '/Users/feichengwang/gitbase/Research/Sam/RA_codes/data/RA_icd.csv',
        index = False
    )
# %%
df = pd.read_csv('/Users/feichengwang/gitbase/Research/Sam/RA_codes/data/RA_icd.csv')
df
# %%
