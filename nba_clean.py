import pandas as pd
pd.options.mode.chained_assignment = None
#pd.set_option('max_columns', None)
import numpy as np
import glob
from tqdm import tqdm


raw_csv_files = glob.glob("data_raw/*.csv")

df_home, df_away = [], []



for file in tqdm(raw_csv_files,desc="Cleaning player data…",):
    df = pd.read_csv(file)

    df = df[(df['GS'] != 'Did Not Play') & (df['GS'] != 'Inactive') & (df['GS'] != 'Did Not Dress') &
            (df['GS'] != 'Player Suspended') & (df['GS'] != 'Player Suspended') & (df['GS'] != 'Not With Team') &
            (df['Rk'] != 'Rk')]

    df['Age'] = df['Age'].str.split('-')
    df['Age'] = df['Age'].str[0].astype(int)*365 + df['Age'].str[1].astype(int)
    df['Age'] = df['Age']/365
    
    df['MP'] = df['MP'].str.split(':')
    df['MP'] = df['MP'].str[0].astype(int)*60 + df['MP'].str[1].astype(int)
    df['MP'] = df['MP']/60

    df['Unnamed: 7'] = df['Unnamed: 7'].str.split(' ')
    df['Game Outcome'] = df['Unnamed: 7'].str[0]
    df['Differential'] = df['Unnamed: 7'].str[1]
    df['Differential'] = df['Differential'].str[1:-1].astype(int)

    df['Unnamed: 5'] = df['Unnamed: 5'].replace('@','1')
    df['Unnamed: 5'] = df['Unnamed: 5'].replace(np.nan,'0')
    df['Away/Home'] = df['Unnamed: 5']

    original_cols = ['Rk', 'G', 'Date', 'Age', 'Tm', 'Unnamed: 5', 'Opp', 'Unnamed: 7', 'GS',
                    'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
                    'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-',
                    'Name', 'Height', 'Weight', 'Year_Born', 'Game Outcome',
                    'Differential']
    
    to_int_cols = ['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB',
                    'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',]

    drop_cols = ['Rk', 'G', 'Unnamed: 5', 'Unnamed: 7','FG%', '3P%', 'FT%', 'Year_Born', 'Height', 'Weight', 'Year_Born']
    
    for col in to_int_cols:
        df[col] = df[col].astype(int)
    
    df = df.drop(drop_cols, axis=1)
    
    df['Score'] = (df['FG']*2 + df['3P']*3 + df['FT']*1 + df['TRB']*1.2 + df['AST']*1.5 + df['BLK']*1.5 + df['STL']*1.5 + df['TOV']*1.5)
        
    df_h = df[df['Away/Home'] == '0']
    df_a = df[df['Away/Home'] == '1']
    
    df_home.append(df_h)
    df_away.append(df_a)
    
    
df_home_master = pd.concat(df_home)
df_away_master = pd.concat(df_away)

df_home_master.to_csv('home_master.csv',index=False)
df_away_master.to_csv('away_master.csv',index=False)




