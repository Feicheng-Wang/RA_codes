'''
Purpose:
    Find out the exact cancer number and hazard ratio under the two categories
    icd 10
        1. "C30-C39": "respiratory and intrathoracic organs"
            C33-C34 Lung
        2. "C81-C96": "lymphoid and hematopoietic tissue"
            C81  Hodgkin's lymphoma
            C82-C88  Nonhodgkin's lymphoma
            C90 Multiple myeloma
            C91-95 leukemia
    icd 9
        1. "160-165": "Respiratory And Intrathoracic Organs"
            162 Lung
        2. "200-208":  "Lymphoid And Hematopoietic Tissue"
            200 Nonhodgkin's lymphoma
            201 Hodgkin's lymphoma
            203 Multiple myeloma
            204-208 leukemia
'''

# %%
cancer_dict = {}
cancer_dict[('C33', 'C34', '162')] = 'Lung'
cancer_dict[('C81', '201')] = "Hodgkin's lymphoma"
cancer_dict[tuple([f'C{num}' for num in range(82, 89)] + ['200'])] = \
    "Nonhodgkin's lymphoma"
cancer_dict[tuple([f'C{num}' for num in range(91, 96)] + 
    [f'{num}' for num in range(204, 209)])] = "Leukemia"

cancer_dict
# %%

# %%
'''
Detail:
    icd 10
        1. "C30-C39": "respiratory and intrathoracic organs"
            C30  Malignant neoplasm of nasal cavity and middle ear
            C31  Malignant neoplasm of accessory sinuses
            C32  Malignant neoplasm of larynx
            C33  Malignant neoplasm of trachea
            C34  Malignant neoplasm of bronchus and lung
            C37  Malignant neoplasm of thymus
            C38  Malignant neoplasm of heart, mediastinum and pleura
            C39  Malignant neoplasm of other and ill-defined sites in the 
                respiratory system and intrathoracic
        2. "C81-C96": "lymphoid and hematopoietic tissue"
            C81  Hodgkin lymphoma
            C82  Follicular lymphoma
            C83  Non-follicular lymphoma
            C84  Mature T/NK-cell lymphomas
            C85  Other specified and unspecified types of non-Hodgkin lymphoma
            C86  Other specified types of T/NK-cell lymphoma
            C88  Malignant immunoproliferative diseases and certain other B-cell lymphomas
            C90  Multiple myeloma and malignant plasma cell neoplasms
            C91  Lymphoid leukemia
            C92  Myeloid leukemia
            C93  Monocytic leukemia
            C94  Other leukemias of specified cell type
            C95  Leukemia of unspecified cell type
            C96  Other and unspecified malignant neoplasms of lymphoid, hematopoietic and related tissue

    icd 9
        1. "160-165": "Respiratory And Intrathoracic Organs"
            160 Malignant neoplasm of nasal cavities middle ear and accessory sinuses
            161 Malignant neoplasm of larynx
            162 Malignant neoplasm of trachea bronchus and lung
            163 Malignant neoplasm of pleura
            164 Malignant neoplasm of thymus heart and mediastinum
            165 Malignant neoplasm of other and ill-defined sites within the respiratory system and intrathoracic organs
        2. "200-208":  "Lymphoid And Hematopoietic Tissue"
            200 Lymphosarcoma and reticulosarcoma and other specified malignant tumors of lymphatic tissue
            201 Hodgkin's disease
            202 Other malignant neoplasms of lymphoid and histiocytic tissue
            203 Multiple myeloma and immunoproliferative neoplasms
            204 Lymphoid leukemia
            205 Myeloid leukemia
            206 Monocytic leukemia
            207 Other specified leukemia
            208 Leukemia of unspecified cell type
'''
