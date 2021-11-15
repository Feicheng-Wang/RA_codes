# survival data

with open(f'../output_data/survival_analysis/{cancer_desc}.pickle', 'rb') as f:
    cancer_icd_list, cancer_desc, treat_survival_df, control_survival_df = \
        pickle.load(f)

treat_survival_df:
cancerFlag	survivalTime	weightN
0	False	72	1
1	False	1771	1
2	False	2198	1
3	False	394	 1