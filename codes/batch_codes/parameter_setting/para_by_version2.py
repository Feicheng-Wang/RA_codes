
# %% 
# import packges
import pickle
import pandas as pd
# from io import StringIO
# %%
# my version
# cancer_dict = {
# tuple(['160', 'C30', 'C31']): 'Malignant neoplasm of nasal cavities, middle ear and accessory sinuses', 
# tuple(['161', 'C32']): 'Malignant neoplasm of larynx', 
# tuple(['162', 'C33', 'C34']):	'Malignant neoplasm of trachea, bronchus and lung', 
# tuple(['163', '164', 'C37', 'C38']): 'Malignant neoplasm of pleura, thymus, heart and mediastinum', 
# tuple(['165', 'C39']):	'Malignant neoplasm of other and ill-defined sites \
# within the respiratory system and intrathoracic organs', 
# tuple(['200', 'C83']): 'Lymphosarcoma and reticulosarcoma', 
# tuple(['201', 'C81']): "Hodgkin's disease", 
# tuple(['202', 'C82', 'C84', 'C85', 'C86', 'C96']): "Other malignant neoplasms of lymphoid and histiocytic tissue", 
# tuple(['203', 'C88', 'C90']): "Multiple myeloma and immunoproliferative neoplasms", 
# tuple(['204', 'C91']): "Lymphoid leukemia", 
# tuple(['205', 'C92']): "Myeloid leukemia", 
# tuple(['206', 'C93']): "Monocytic leukemia",
# tuple(['207', 'C94']): "Other specified leukemia",
# tuple(['208', 'C95']): "Leukemia of unspecified cell type"
# }

cancer_dict = {
tuple(['172', 'C43']): 'Malignant melanoma of skin', 
tuple(['173', 'C44']): 'Other and unspecified malignant neoplasm of skin', 
tuple(['160', 'C30', 'C31']): 'Malignant neoplasm of nasal cavities, middle ear and accessory sinuses', 
tuple(['161', 'C32']): 'Malignant neoplasm of larynx', 
tuple(['162', 'C33', 'C34']):	'Malignant neoplasm of trachea, bronchus and lung', 
tuple(['162.0', 'C33']): 'Malignant neoplasm of trachea', 
tuple(['162.2', 'C34.0']):	'Malignant neoplasm of main bronchus', 
tuple(['162.3', '162.4', '162.5', '162.8', '162.9', 'C34.1', 
    'C34.2', 'C34.3', 'C34.8', 'C34.9']): \
    'Malignant neoplasm of lung and other parts of bronchus', 
tuple(['163', '164', 'C37', 'C38']): 'Malignant neoplasm of pleura, thymus, heart and mediastinum', 
tuple(['165', 'C39']):	'Malignant neoplasm of other and ill-defined sites \
within the respiratory system and intrathoracic organs', 
# tuple(['200', 'C83']): 'Lymphosarcoma and reticulosarcoma', 
tuple(['201', 'C81']): "Hodgkin's disease", 
tuple(['200', '202', 'C82', 'C83', 'C84', 'C85', 'C86', 'C96']): "Other malignant neoplasms of lymphoid and histiocytic tissue", 
tuple(['203', 'C88', 'C90']): "Multiple myeloma and immunoproliferative neoplasms", 
tuple(['204', 'C91']): "Lymphoid leukemia", 
tuple(['205', 'C92']): "Myeloid leukemia", 
tuple(['206', 'C93']): "Monocytic leukemia",
tuple(['207', 'C94']): "Other specified leukemia",
tuple(['208', 'C95']): "Leukemia of unspecified cell type"
}

df = pd.DataFrame(cancer_dict.items(), columns=['ICD List', 'Cancer Type'])
df = df[['Cancer Type', 'ICD List']]
df.to_csv('/Users/feichengwang/gitbase/Research/Sam/RA_codes/output_data/cancer_focus_icd.csv', index=False)
# %%
for cancer_icd_list, cancer_desc in cancer_dict.items():
    with open('{}.pickle'.format(cancer_desc), 'wb') as f:
        pickle.dump((list(cancer_icd_list), cancer_desc), f)

# %%
# tell us the mapping between icd9 and icd10
# import pandas as pd
# df = pd.read_csv('../data/icd10cmtoicd9gem.csv')
# df['icd9'] = df['icd9cm'].apply(lambda x: x[:3])
# df['icd10'] = df['icd10cm'].apply(lambda x: x[:3])
# df = df[['icd9', 'icd10']]
# df.drop_duplicates(inplace=True)
# df = df[df['icd9'].isin([str(x) for x in range(200, 209)] + [str(x) for x in range(160, 166)])]
# output_df = pd.DataFrame(df.groupby('icd9')['icd10'].apply(lambda x: list(x)).rename('icd10'))
# output_df.to_csv('../output/icd9_10_mapping.csv')
# output_df.apply(lambda x: [x.name] + x['icd10'], axis=1)

# %%
