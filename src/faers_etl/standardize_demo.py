import pandas as pd
import numpy as np

def age_to_years(age, code):
    try:
        a = float(age)
    except:
        return np.nan
    mapping = {
        'DEC': a*12, 'MON': a/12, 'WK': a/52, 'DY': a/365, 'HR': a/8760
    }
    return round(mapping.get(code.upper(), a), 2)

def main():
    demo = pd.read_csv('data/interim/DEMO_Combined.csv', dtype=str)
    drug = pd.read_csv('data/interim/DRUG_Combined.csv', dtype=str)
    # ... load other combined files as needed
    demo['AGE_Years_fixed'] = demo.apply(lambda r: age_to_years(r['AGE'], r['AGE_COD']), axis=1)
    # country mapping stub
    demo['COUNTRY_CODE'] = demo['REPORTER_COUNTRY']
    demo.loc[demo['COUNTRY_CODE'].isin(['UNK','NS','YR']), 'COUNTRY_CODE'] = np.nan
    demo['Gender'] = demo['GNDR_COD'].replace({'UNK':np.nan,'NS':np.nan,'YR':np.nan})
    # dedup logic...
    demo.to_csv('data/interim/DEMO_Aligned.csv', index=False)
    print("Saved DEMO_Aligned.csv")

if __name__ == "__main__":
    main()
