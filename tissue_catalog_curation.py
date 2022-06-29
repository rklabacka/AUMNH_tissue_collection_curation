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
    tube_note = str(tube_note).lower()
    re_str = r'(?:tail scute|toenail|toe webbing|smooth muscle|peletted rbc|liver|muscle|tail|brain|lungs|testes|eyeballs|heart|kidneys|skin|stomach|gall bladder|webbing|toe|scute|gill|whole animal)'
    re_obj = re.compile(re_str)
    if re_obj.search(tube_note):
        search_result = re_obj.search(tube_note)
        print(search_result.group())
        return search_result.group()
    else:
        return ""

def modify_collector_names(df):
    stiles_re = re.compile('(?:Stiles James)|(?:J\+S Stiles)|(?:Jimmy Siltes)|(?:Stiles J)|(?:Stiles)|(?:J. Stiles)|(?:Jimmy Stiles)|(?:James Stiles)|(?:J.A. Stiles)')
    laurencio_re = re.compile('D. Laurencio')
    godwin_re = re.compile('(?:J.C. Godwin)|(?:James Godwin)|(?:James C Godwin)')
    birkhead_re = re.compile('(?:Roger D Birkhead)|(?:R. Birkhead)|(R Birkhead)|(Roger Birkhead)|(?:Birkhead)')
    goessling_re = re.compile('(?:Goessling)|(?:J Goessling)|(Jeff Goessling)')
    goetz_re = re.compile('(?:Scott M Goetz)|(Scott Goetz)')
    folt_re = re.compile('(?:B Folt)|(?:Brian Folt)|(?:Brian P Folt)|(?:PPF)|(?:Folt B)|(?:B. Folt)')
    andreadis_re = re.compile('(?:Andreadis P)|(?:P. T. Andreadis)|(Paul Andreadis)')
    cobb_re = re.compile('Kerry A Cobb')
    jenkins_re = re.compile('(?:A.J Jenkins|(?:A Joseph Jenkins)|(?:Arthur J Jenkins)|(?:A.J. Jenkins)|(?:Jenkins)|(?A. Joe Jenkins)')
    melissa_re = re.compile('(?:Melissa Miller)|(?:Melissa A Miller)|(Miller)')
    #white_re = re.compile('(?:Steve S White)')
    chivers_re = re.compile('(?:Jacqueline M Chivers)')
    werneke_re = re.compile('(?:David C Werneke)|(?:Werneke)')
    klabacka_re = re.compile('')
    pierson_re = re.compile('T Pierson')
    picilomini_re = re.compile('S Picilomini')
    sanspree_re = re.compile('(?:Colt R Sanspree)|(?:Colt Sanspree)')
    stiles2_re = re.compile('(?:S. Stiles)')
    hanslowe_re = re.compile('(?:Emma Hanslow)')
    dalton_re = re.compile('(?:Jay W Dalton)')
    holt_re = re.compile('(?:Brian Holt)|(?:Brian D Holt)')
    df['verbatum_collector'] = df['verbatum_collector'].str.replace(', and ',',')
    df['verbatum_collector'] = df['verbatum_collector'].str.replace(' and ',',')
    df['verbatum_collector'] = df['verbatum_collector'].str.replace(' \& ',',')
    primary_collector = df['verbatum_collector'].str.split(",|;", expand = True)[0]
    primary_collector = primary_collector.str.replace(stiles_re,'James A. Stiles')
    primary_collector = primary_collector.str.replace(laurencio_re,'David Laurencio')
    primary_collector = primary_collector.str.replace(godwin_re,'James C. Godwin')
    primary_collector = primary_collector.str.replace(birkhead_re,'Roger D. Birkhead')
    primary_collector = primary_collector.str.replace(folt_re,'Brian P. Folt')
    primary_collector = primary_collector.str.replace(goetz_re,'Scott M. Goetz')
    primary_collector = primary_collector.str.replace(andreadis_re,'Paul T. Andreadis')
    primary_collector = primary_collector.str.replace(goessling_re,'Jeffrey Goessling')
    primary_collector = primary_collector.str.replace(cobb_re,'Kerry A. Cobb')
    primary_collector = primary_collector.str.replace(jenkins_re,'Arthur J. Jenkins')
    primary_collector = primary_collector.str.replace(melissa_re,'Melissa A. Miller')
    #primary_collector = primary_collector.str.replace(white_re,'Steve S. White')
    primary_collector = primary_collector.str.replace(chivers_re,'Jacqueline M. Chivers')
    primary_collector = primary_collector.str.replace(pierson_re,'Todd Pierson')
    primary_collector = primary_collector.str.replace(werneke_re,'David C. Werneke')
    primary_collector = primary_collector.str.replace(picilomini_re,'Sara Picilomini')
    primary_collector = primary_collector.str.replace(sanspree_re,'Colt R. Sanspree')
    primary_collector = primary_collector.str.replace(stiles2_re,'Sierra Stiles')
    primary_collector = primary_collector.str.replace(hanslowe_re,'Emma Hanslowe')
    primary_collector = primary_collector.str.replace(dalton_re,'Jay W. Dalton')
    primary_collector = primary_collector.str.replace(holt_re,'Brian D. Holt')
    df.loc[df['collector_last_name'].str.strip() == '', 'collector_last_name'] = df['verbatum_collector'].apply(parse_collector_name)
    return df

def parse_collector_name(verbatum_collector):
    primary_collector = verbatum_collector.split(",")[0]
    primary_collector_split = primary_collector.split(".")


if __name__ == "__main__":
    tissue_df = import_file(sys.argv[1])
    tissue_df = edit_column_names(tissue_df)
    tissue_df = add_tissue_type(tissue_df)



