import pandas as pd
import re
import gspread
from rapidfuzz import fuzz 
from rapidfuzz import process 
import os
from dotenv import load_dotenv, find_dotenv

# get the path to the Quotes & Question markdown files in Obsidian folder
load_dotenv(find_dotenv())
quotes_path = os.environ.get('QUOTES_NOTE_PATH')
qs_path = os.environ.get('QUESTIONS_NOTE_PATH')
folder_id = os.environ.get('GDRIVE_FOLDER_ID')

# Authorizing to my google cloud
gc = gspread.oauth()

def markdown_to_df(file_path, delimiter, col_name):
    # Read the markdown file
    with open(file_path, 'r', encoding="utf8") as f:
        content = f.read()

    raw_strs = content.split(delimiter)[1:]

    str_list = [q for q in raw_strs if q != '']
    df = pd.DataFrame(str_list, columns=[col_name])
    df['Score'] = 0
    return df


def write_gsheet(gsheet_name, folder_id, col_name, df):
    gsheet = gc.open(gsheet_name, folder_id=folder_id)
    worksheet = gsheet.get_worksheet(0)
    og_df = pd.DataFrame(worksheet.get_all_records())

    min_score = min(og_df.Score) + 1

    for q, s in df[[col_name, 'Score']].values:
        
        og_match = process.extractOne(q, og_df[col_name], score_cutoff=90)
        if og_match is None:
            df.loc[df[col_name] == q, 'Score'] = min_score
        else:
            df.loc[df[col_name] == q, 'Score'] = og_df.loc[og_df[col_name] == og_match[0], 'Score'].values[0]
    
    # clear the spreadsheet and insert new table into the spreadsheet
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


# Writing the quotes
quotes_df = markdown_to_df(quotes_path, '\n', 'Quote')
write_gsheet('quotes', folder_id, 'Quote', quotes_df)

# Writing the questions
qs_df = markdown_to_df(qs_path, '\n', 'Questions')
write_gsheet('questions', folder_id, 'Questions', qs_df)
