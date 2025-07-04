import os
import pandas as pd

# Define schemas for FAERS tables
SCHEMAS = {
    'DRUG': ['ISR','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM'],
    'REAC': ['ISR','PT'],
    'DEMO': ['ISR','CASE','I_F_COD','FOLL_SEQ','IMAGE','EVENT_DT','MFR_DT','FDA_DT','REPT_COD','MFR_NUM','MFR_SNDR','AGE','AGE_COD','GNDR_COD','E_SUB','WT','wt_COD','REPT_DT','OCCP_COD','DEATH_DT','TO_MFR','CONFID','REPORTER_COUNTRY'],
    'OUTC': ['primaryid','caseid','OUTC_COD'],
    'INDI': ['ISR','DRUG_SEQ','INDI_PT'],
    'THER': ['ISR','DRUG_SEQ','START_DT','END_DT','DUR','DUR_COD'],
    'RPSR': ['ISR','RPSR_COD']
}

BASE_DIR = os.path.abspath('data/raw')

def read_quarter(table, year, quarter):
    q2 = quarter.lower()
    yy = str(year)[-2:]
    fname = f"{table}{yy}{quarter}.TXT"
    path = os.path.join(BASE_DIR, f"aers_ascii_{year}q{q2}", 'ascii', fname)
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, sep='$', header=None, names=SCHEMAS[table], dtype=str, engine='python', na_values=[''])
    df['PERIOD'] = f"{yy}{quarter}"
    return df

def main():
    years = range(2004, 2022)
    quarters = ['Q1','Q2','Q3','Q4']
    for table, cols in SCHEMAS.items():
        parts = []
        for year in years:
            for q in quarters:
                df = read_quarter(table, year, q)
                if df is not None:
                    parts.append(df)
        if parts:
            combined = pd.concat(parts, ignore_index=True)
            # clean OUTC_COD
            if table == 'OUTC':
                combined['OUTC_COD'] = combined['OUTC_COD'].str.replace(r"[\$\r\n\t]", "", regex=True).str.strip()
            combined.to_csv(f"data/interim/{table}_Combined.csv", index=False)
            print(f"Saved {table}_Combined.csv with {combined.shape[0]} rows.")

if __name__ == "__main__":
    main()
