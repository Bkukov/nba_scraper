from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

def get_season_data():
    """ Extract table contents and player details in order to create a
        list of dataframes for batching and saving into CSVs """

    url = "https://www.basketball-reference.com"
    season_list = create_player_season_list()
    df_list = []
    counter = 0

    for season in tqdm(season_list,desc="Extracting season data…",):
        details = []
        link = url + season

        raw_html = requests.get(link).text
        soup = BeautifulSoup(raw_html, 'lxml')

        div = soup.find('div', {'id':'meta'})
        for span in div.find_all('span'):
            details.append(span.text.strip('\n'))

        header_split = details[0].split(' ')
        name = header_split[0]+' '+header_split[1]

        df = pd.read_html(link)
        df_season = df[-1].copy()

        df_season['Name'] = name
        df_season['Height'] = details[1]
        df_season['Weight'] = details[2]
        df_season['Year_Born'] = details[3][-4:]

        df_list.append(df_season)

        if len(df_list)%50==0:
            df = pd.concat(df_list)
            df.to_csv(f'data_raw/batch_{counter}.csv', index=False)
            df_list = []
            counter+=1

    df = pd.concat(df_list)
    df.to_csv(f'data_raw/batch_{counter}.csv', index=False)

    return


def create_player_season_list():
    """ Create a list of links by player href that will get me to
        individual season page"""

    url = "https://www.basketball-reference.com"

    href_list = create_player_href_list()
    per_game_list = []

    for href in tqdm(href_list,desc="Extracting player hrefs…",):

        link = url + href

        raw_html = requests.get(link).text
        soup = BeautifulSoup(raw_html, 'lxml')

        table = soup.find('table', {'id':'per_game'})
        for tr in table.find_all('tr'):
            try:
                tr_text = tr.find('a').get('href')
                if tr_text[1:8] == 'players':
                    per_game_list.append(tr_text)
            except:
                continue

    return per_game_list


def create_player_href_list():
    """ Create a list of links by player href that will get me to
        individual player page"""

    link_list = create_link_list()

    href_list = []

    for link in tqdm(link_list,desc="Extracting player links…",):

        raw_html = requests.get(link).text
        soup = BeautifulSoup(raw_html, 'lxml')

        table = soup.find('table', {'id':'players'})
        for strong in table.find_all('strong'):
            href_list.append(strong.find('a').get('href'))

    return href_list


def create_link_list():
    """ Create a list of links by letter that will get me to href
        page for individual players """

    url = "https://www.basketball-reference.com/players/"
    letters = ['A','B','C','D','E','F','G','H','I','J','K',
                'L','M','N','O','P','Q','R','S','T','U','V',
                'W','X','Y','Z',]

    link_list = []

    for letter in letters:
        link_list.append(url+letter.lower())

    return link_list


if __name__ == '__main__':
    get_season_data()
