#! /usr/env/bin/ python

"""
Script to import and curate the AUMNH tissue catalog.
Output file is ready to be uploaded to Specify.
"""

import pandas as pd
import sys
import re

def import_file(excel_file_name):
    df = pd.read_excel(excel_file_name)
    return df

def edit_column_names(df):
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return df

def add_tissue_type(df):
    df.loc[df['tissue_type'].str.strip() == '', 'tissue_type'] = df['tube_notes'].apply(check_tissue_note)
    return df

def check_tissue_note(tube_note):
    print("within function")
    tube_note = str(tube_note).lower()
    re_str = r'(?:tail scute|toenail|toe webbing|smooth muscle|peletted rbc|liver|muscle|tail|brain|lungs|testes|eyeballs|heart|kidneys|skin|stomach|gall bladder|webbing|toe|scute|gill|whole animal)'
    re_obj = re.compile(re_str)
    if re_obj.search(tube_note):
        search_result = re_obj.search(tube_note)
        print(search_result.group())
        return search_result.group()
    else:
        return ""


if __name__ == "__main__":
    tissue_df = import_file(sys.argv[1])
    tissue_df = edit_column_names(tissue_df)
    tissue_df = add_tissue_type(tissue_df)



