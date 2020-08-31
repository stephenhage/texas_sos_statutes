import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

datadir = Path.home() / "Github/texas_sos_statutes/statutes/data/"

# read the ontology sheet
def _read_ontology_data(filename, sheetname, header_row):
    return pd.read_excel(datadir / filename, sheetname, header = header_row)

# read the simple statutes and regulations
def _read_legal_data(filename):
    return pd.read_csv(datadir / filename, sep = "|")

# choose an encoder model
def _create_embedder(model):
    return SentenceTransformer(model)

# encode text
def _encode_text(filename, column, model):
    embedder = _create_embedder(model)
    df = _read_legal_data(filename)
    df['encoded_text'] = embedder.encode(df[column]).tolist()
    return df

# calculate similarity of the onotology words to each statute/regulation
def _similarity_scoring(ontology_df, filename, column, titlecol, model):
    legal_df = _encode_text(filename, column, model)
    n = 0
    for text in ontology_df.Reason.tolist():
        embedder = _create_embedder(model)
        query = embedder.encode(text)
        if n == 0:
            copy_legal_df = legal_df.copy()
            print(copy_legal_df.head())
            copy_legal_df['similarity'] = np.round(cosine_similarity(query, list(copy_legal_df['encoded_text']))[0], 5)
            copy_legal_df['reason'] = text
            copy_legal_df = copy_legal_df.sort_values('similarity', ascending = False).drop_duplicates([titlecol]).head()
            n += 1
        else:
            new_legal_df = legal_df.copy()
            print(new_legal_df.head())
            new_legal_df['similarity'] = np.round(cosine_similarity(query, list(new_legal_df['encoded_text']))[0], 5)
            new_legal_df['reason'] = text
            new_legal_df = new_legal_df.sort_values('similarity', ascending=False).drop_duplicates([titlecol]).head()
            copy_legal_df = pd.concat([copy_legal_df, new_legal_df], axis = 1, ignore_index = True)
            n += 1
    return legal_df

# for top statutes/reg, select the subsection exploded version and do the same process, show top 5 subsections
def _similarity_scoring_subsection(ontology_df, similarity_df, exploded_df):
    applicable_reg = similarity_df.sort_values('similarity', ascending = False).citation.iloc[0]
    legal_df = exploded_df.iloc[exploded_df.citation == applicable_reg,]
    n = 0
    for text in ontology_df.Reason.tolist():
        embedder = _create_embedder(model)
        query = embedder.encode(text)
        if n == 0:
            legal_df['similarity'] = np.round(cosine_similarity(query, list(legal_df['encoded_text']))[0], 5)
            legal_df['reason'] = reason
            legal_df = legal_df.sort_values('similarity', ascending=False).drop_duplicates([titlecol]).head()
            n += 1
        else:
            new_legal_df = legal_df.copy()
            new_legal_df['similarity'] = np.round(cosine_similarity(text, list(legal_df['encoded_text']))[0], 5)
            new_legal_df['reason'] = reason
            new_legal_df = legal_df.sort_values('similarity', ascending=False).drop_duplicates([titlecol]).head()
            legal_df = pd.concat([legal_df, new_legal_df], axis=1, ignore_index=True)
            n += 1
    return legal_df

statutes = _read_legal_data("clean_statutes_preprocessed.csv")
regs = _read_legal_data("clean_regs_preprocessed.csv")
ontology = _read_ontology_data("ontology_template.xlsx", sheetname="Reasons", header_row = 1)
MODEL = 'bert-base-nli-mean-tokens'
# statutes = _encode_text(df = statutes, column = "section_text", model = MODEL)
# print(statutes['encoded_text'])
statutes_similarity = _similarity_scoring(ontology_df=ontology,
                                          filename = "clean_statutes_preprocessed.csv",
                                          column = "section_text", titlecol="section_title", model=MODEL)
# [print(f"{x}\n") for x in statutes_similarity.columns]
statutes_similarity.to_csv(datadir/"statute_similarity_ontology.csv")
#
# regs = _encode_text(df = regs, column = "regulation_text", model = MODEL)
reg_similarity = _similarity_scoring(ontology_df=ontology, filename="clean_regs_preprocessed.csv",
                                     column = "regulation_text",
                                     titlecol="service_type", model=MODEL)
reg_similarity.to_csv(datadir/"regs_similarity_ontology.csv")

