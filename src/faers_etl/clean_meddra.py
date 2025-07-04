import os
import re
import pandas as pd

MEDDRA_DIR = os.path.abspath('data/raw/meddra')
SCHEMAS = {
    'llt': ['llt_code','llt_name','pt_code','llt_whoart_code','llt_harts_code','llt_costart_sym','llt_icd9_code','llt_icd9cm_code','llt_icd10_code','llt_currency','llt_jart_code'],
    'pt': ['pt_code','pt_name','null_field','pt_soc_code','pt_whoart_code','pt_harts_code','pt_costart_sym','pt_icd9_code','pt_icd9cm_code','pt_icd10_code','pt_jart_code']
}

def read_meddra(table):
    path = os.path.join(MEDDRA_DIR, table + '.asc')
    return pd.read_csv(path, sep='\$', header=None, names=SCHEMAS[table], dtype=str, engine='python', na_values=[''])

def main():
    low = read_meddra('llt')
    pref = read_meddra('pt')
    df_indi = pd.read_csv('data/interim/INDI_Combined.csv', dtype=str)
    df_reac = pd.read_csv('data/interim/REAC_Combined.csv', dtype=str)

    for df, name in [(df_indi, 'INDI'), (df_reac, 'REAC')]:
        df['CLEANED_PT'] = df[name + '_PT' if name=='INDI' else 'PT'].astype(str).replace(r'[\r\n\t]', '', regex=True).str.strip().str.upper()
        df['MEDDRA_CODE'] = pd.NA
        # join on pref
        merged = df.merge(pref[['pt_name','pt_code']], left_on='CLEANED_PT', right_on='pt_name', how='left')
        df['MEDDRA_CODE'] = merged['pt_code']
        # join on llt
        merged = df.merge(low[['llt_name','llt_code']], left_on='CLEANED_PT', right_on='llt_name', how='left')
        df['MEDDRA_CODE'] = df['MEDDRA_CODE'].fillna(merged['llt_code'])
        # manual overrides
        df.to_csv(f"data/interim/{name}_Combined_cleaned.csv", index=False)
        print(f"Saved {name}_Combined_cleaned.csv")

if __name__ == "__main__":
    main()
