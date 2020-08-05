import pandas as pd
import re
from pathlib import Path

def _open_file(file):
    with open(file) as f:
        statutes = f.read()
    return statutes

def _create_re():
    return r"(Sec. [0-9]{3}.[0-9]+)(.*)(\n)"

def _extract_matches(file):
    f = _open_file(file)
    p = _create_re()
    return re.findall(p, f)

def make_dataframe_statutes(file):
    dat = _extract_matches(file)
    df = pd.DataFrame(dat, columns = ["Section", "Text", "Disregard"])
    return df[["Section", "Text"]]

def _remove_sec_from_section(df):
    df['Section'] = df["Section"].str.replace("Sec. ", "")
    return df

def _split_section(df):
    df = _remove_sec_from_section(df)
    df[["Section", "Subsection"]] = df.Section.str.split(".", expand = True)
    return df

def _split_text_header(df):
    df = _split_section(df)
    df[["Section_Title", "Section_Text"]] = df.Text.str[1:].str.replace('"', "").str.split(".", 1, expand = True)
    return df[["Section", "Subsection", "Section_Title", "Section_Text"]]

datadir = Path.home() / "Github" / "texas_sos_statutes" / "statutes" / "data"
df = make_dataframe_statutes(datadir /"statutes_text.txt")
df = _split_text_header(df)
df.to_excel((datadir / "clean_statutes.xlsx"), index = False, sheet_name = "cleaned_statutes")