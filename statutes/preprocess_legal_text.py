import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nlp
import os
import re
from pathlib import Path

def get_datadir():
    return Path.home() / "Github/texas_sos_statutes/statutes/data/"

def _open_file(filename):
    datfile = get_datadir() / filename
    if datfile.suffix == ".csv":
        return pd.read_csv(datfile, sep = "|")
    else:
        return pd.read_excel(datfile)

def _clean_names(df):
    df.columns = [re.sub(r"[^a-z]", "_", x.lower()) for x in df.columns]
    return df

def _standardize_case(df, col):
    return df[col].str.lower()

def _split_statute_subsections(df, textcol):
    df['text'] = df[textcol].str.split(r"(\([a-zA-Z0-9][\-0-9]?\) )")
    df = df.explode('text').reset_index()
    df.text = df.text.str.strip()
    return df

def _add_subsection_reference(df):
    df['subsection_letter'] = ''
    df.loc[df.text.str.contains(r"^\("), "letter"] = df.text
    df.letter = df.letter.fillna(method="ffill")
    df.letter = df.letter.fillna("(a)")
    return df

def _clean_typo_section(df, typocol_one = None, typocol_two = None):
    if typocol_one and typocol_two:
        clean_df = df.loc[df[typocol_two].isnull(),][typocol_one].str.split("\(", expand=True)
        tuples = [tuple(x) for x in clean_df.to_numpy()]
        df.loc[df[typocol_two].isnull(), [typocol_one, typocol_two]] = tuples
        return df
    else:
        return df

def _remove_blank_subections(df):
    df = _clean_names(df)
    if "subsection" in df.columns:
        df = df.loc[~df.text.str.isspace(),]
    else:
        df = df.loc[df.text != "", ]
    return df

def _create_citation(df, colslist):
    if "subsection" in df.columns:
        df['citation'] = df.section.astype(str) + "." + df.subsection.astype(int).astype(str) + "." + df.letter.str.strip().str.replace(r"\W", "")
    else:
        df['citation'] = df.regulation.astype(str) + "." + df.letter.str.strip().str.replace(r"\W", "")
    return df[colslist]

def standard_set_legal_data(filename, standard_col = None):
    df = _open_file(filename)
    df = _clean_names(df)
    if standard_col:
        df[col] = _standardize_case(df, col)
        return df
    else:
        return df

def subsection_split_data(filename, standard_col = None):
    print(f"opening {filename}")
    df = _open_file(filename)
    print("cleaning names")
    df = _clean_names(df)
    print(f"cleaned names: {[x for x in df.columns]}")
    if "statute" in filename:
        textcol = "section_text"
        output_cols = ['citation', 'section_title',	'text']
        typocols = ['section', 'subsection']
    else:
        textcol = "regulation_text"
        output_cols = ['citation', 'service_type', 'urls', 'text', ]
        typocols = list()
    print(f"working on: \n{textcol}\n{output_cols}\n{typocols}")
    if standard_col:
        df[standard_col] = _standardize_case(df, standard_col)
    print(f"splitting into subsections {df.columns}")
    df = _split_statute_subsections(df, textcol=textcol)
    print(f"adding the subsection reference")
    df = _add_subsection_reference(df)
    print(f"fixing weird typos for {filename}")
    if typocols:
        df = _clean_typo_section(df, typocols[0], typocols[1])
    print(f"clearing out blank subsections for {filename}")
    df = _remove_blank_subections(df)
    print(f"column names: {[x for x in df.columns]}")
    print(f"assembling the citation for {filename}")
    df = _create_citation(df, output_cols)
    return df

datdir = get_datadir()
df = standard_set_legal_data("tx_sales_tax_regulations.csv")
df.to_csv(datdir / "clean_regs_preprocessed.csv", sep = "|")

df = subsection_split_data("tx_sales_tax_regulations.csv")
df.to_csv(datdir / "clean_regs_split_subsections.csv", sep = "|")

df = standard_set_legal_data("clean_statutes.xlsx")
df.to_csv(datdir / "clean_statutes_preprocessed.csv", sep = "|")
df = subsection_split_data("clean_statutes.xlsx")
df.to_csv(datdir / "clean_statutes_split_subsections.csv", sep = "|")

