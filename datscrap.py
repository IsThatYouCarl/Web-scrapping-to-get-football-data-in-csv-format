import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_table(url_league, df):
    for year in range(1992, 2024):
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KTML, Like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        url = f'{url_league}{year}'
    
        page = requests.get(url, headers = headers)
        soup_o = BeautifulSoup(page.text, "lxml")
        soup = soup_o.findAll("div", attrs = {"id":"yw1"})[0]
    
        Ranks = soup.findAll("td", attrs = {"class": "rechts hauptlink"})
        Teams = soup.findAll("td", attrs = {"class": "no-border-links hauptlink"})
        Scores = soup.findAll("td", attrs = {"class": "zentriert"}) #MD W D L remove  GD  P

        Ranks_list = []
        for rank in Ranks:
            Ranks_list.append(rank.text)

        Teams_list = []
        for team in Teams:
            Teams_list.append(team.text.strip())
            
        master_scores = []
        def score_scrap(Scores):   
            sub_scores = []
            if len(Scores) == 0:
                return '0'
            if len(Scores) <= 8:
                for score in Scores:
                    sub_scores.append(score.text)
                master_scores.append(sub_scores)      
            else:
                for i, score in enumerate(Scores):        
                    if i > 7:
                        master_scores.append(sub_scores)
                        Scores_new = Scores[8:]  
                        score_scrap(Scores_new)
                        break            
                    sub_scores.append(score.text)

        score_scrap(Scores)

        for i in range(len(master_scores)):
            new_row =  {'Season_End_Year': year+1, 'Team': Teams_list[i], 'Rank': Ranks_list[i], 'MP': master_scores[i][1], 'W': master_scores[i][2], 'D': master_scores[i][3], 'L': master_scores[i][4], 'GD': master_scores[i][6], 'Pts': master_scores[i][7]}
            df.loc[len(df)] = new_row

        print(year)

def get_bundesliga():
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    get_table('https://www.transfermarkt.com/bundesliga/tabelle/wettbewerb/L1?saison_id=', df)
    csv_path = 'bundesliga-league-tables.csv'
    df.to_csv(csv_path, index = False)
    
def get_serieA():
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    get_table('https://www.transfermarkt.com/serie-a/tabelle/wettbewerb/IT1?saison_id=', df)
    csv_path = 'serieA-league-tables.csv'
    df.to_csv(csv_path, index = False)

def get_laliga():
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    get_table('https://www.transfermarkt.com/laliga/tabelle/wettbewerb/ES1?saison_id=', df)
    csv_path = 'laliga-league-tables.csv'
    df.to_csv(csv_path, index = False)
    
def get_ligue1():
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    get_table('https://www.transfermarkt.com/ligue-1/tabelle/wettbewerb/FR1?saison_id=', df)
    csv_path = 'ligue1-league-tables.csv'
    df.to_csv(csv_path, index = False)

def get_premier_league():
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    get_table('https://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=', df)
    csv_path = 'premier-league-tables.csv'
    df.to_csv(csv_path, index = False)

# get_bundesliga()
# get_laliga()
# get_ligue1()
# get_serieA()
get_premier_league()