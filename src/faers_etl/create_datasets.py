import pandas as pd
import numpy as np

def main():
    drug_map3 = pd.read_csv('data/processed/DRUG_MAPPER_3.csv', dtype=str)
    aligned = pd.read_csv('data/interim/DEMO_Aligned.csv', dtype=str)
    # Example: DRUGS_STANDARDIZED
    drugs_std = drug_map3.loc[
        (drug_map3['FINAL_RXAUI'].notna())&
        (drug_map3['primaryid'].isin(aligned['primaryid'])),
        ['primaryid','DRUG_ID','DRUG_SEQ','ROLE_COD','PERIOD','FINAL_RXAUI','REMAPPING_STR']
    ].drop_duplicates()
    drugs_std.to_csv('data/processed/DRUGS_STANDARDIZED.csv', index=False)
    print("Created DRUGS_STANDARDIZED.csv")
    # ... implement other dataset tables similarly

if __name__ == "__main__":
    main()
