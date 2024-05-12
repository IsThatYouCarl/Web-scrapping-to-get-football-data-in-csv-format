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

def get_topscorer(Season, League, Nationality, Age_Group, Position, Main_Position, page):
    saison_id = int(Seasons[Season])
    OptionKey = int(League_groups[League])

    altersklasse_val = Age_group[Age_Group]
    if altersklasse_val == "":
        altersklasse = altersklasse_val
    else:
        altersklasse = int(altersklasse_val)

    aurischtung_val = Position_groups[Position]
    if aurischtung_val == "":
        aurischtung = aurischtung_val
    else:
        aurischtung = int(aurischtung_val)

    spielerposition_id_val = Main_position_list[Main_Position]
    if spielerposition_id_val == "":
        spielerposition_id = spielerposition_id_val 
    else:
        spielerposition_id = int(spielerposition_id_val)

    land_id = int(Nationality_list[Nationality])

    if str(page) == "All":
        df_top_scorer =  pd.DataFrame(columns = ['Rank','Name', 'Age', 'Club', 'Matches', 'Goals'])
        info = f'Season = {Season}, League = {League}, Nationality = {Nationality}, Age Group = {Age_Group}, Position = {Position}, Main Position = {Main_Position}, Number of pages = {page}'
        current_page = 1
        print(f"Created a dataframe for {info}")
        while True:
            url = f'https://www.transfermarkt.com/scorer/toptorschuetzen/statistik/2023/plus/0/galerie/0?saison_id={saison_id}&selectedOptionKey={OptionKey}&land_id={land_id}&altersklasse={altersklasse}&ausrichtung={aurischtung}&spielerposition_id={spielerposition_id}&yt0=Show/plus/0/galerie/0/page/{current_page}'
            top_scorer_collection(df_top_scorer, url)
            print(f'page = {current_page}')
            current_page +=1

    else:        
        df_top_scorer =  pd.DataFrame(columns = ['Rank','Name', 'Age', 'Club', 'Matches', 'Goals'])
        info = f'Season = {Season}, League = {League}, Nationality = {Nationality}, Age Group = {Age_Group}, Position = {Position}, Main Position = {Main_Position}, Number of pages = {page}'
        print(f"Created a dataframe for {info}")
        for current_page in range(1, page+1):
            url = f'https://www.transfermarkt.com/scorer/toptorschuetzen/statistik/2023/ajax/yw1/saison_id/{saison_id}/selectedOptionKey/{OptionKey}/land_id/{land_id}/altersklasse/{altersklasse}/ausrichtung/{aurischtung}/spielerposition_id/{spielerposition_id}/yt0/Show/plus/0/galerie/0/page/{current_page}'
            print(url)
            top_scorer_collection(df_top_scorer, url)
            print(f'page = {current_page}')

    csv_path = 'top_scorer.csv'
    df_top_scorer.to_csv(csv_path, index = False)


def top_scorer_collection(df_top_scorer, url):   
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KTML, Like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.text, "lxml")

    odd_list = []
    even_list = []
    odds = soup.findAll("tr", attrs = {"class": "odd"})
    evens = soup.findAll("tr", attrs = {"class": "even"})

    for odd in odds:
        player_list = []
        rank = odd.findAll("td", attrs={"class":"zentriert"})[0]
        age = odd.findAll("td", attrs={"class":"zentriert"})[1]
        matches = odd.findAll("td", attrs={"class":"zentriert"})[3]

        goals = odd.findAll("td", attrs={"class": "zentriert hauptlink"})[0]

        name = odd.findAll("td", attrs = {"class":"hauptlink"})[0]
        club = odd.findAll("td", attrs = {"class":"hauptlink"})[1]
        player_list = [rank.text.strip(), name.text.strip(), club.text.strip(), age.text.strip(), matches.text.strip(), goals.text.strip()]
        odd_list.append(player_list)

    for even in evens:
        player_list = []
        rank =even.findAll("td", attrs={"class":"zentriert"})[0]
        age = even.findAll("td", attrs={"class":"zentriert"})[1]
        matches = even.findAll("td", attrs={"class":"zentriert"})[3]

        goals = even.findAll("td", attrs={"class": "zentriert hauptlink"})[0]

        name = even.findAll("td", attrs = {"class":"hauptlink"})[0]
        club = even.findAll("td", attrs = {"class":"hauptlink"})[1]
        player_list = [rank.text.strip(), name.text.strip(), club.text.strip(), age.text.strip(), matches.text.strip(), goals.text.strip()]
        even_list.append(player_list)

    master_list = []
    for i in range(max(len(odd_list), len(even_list))):
        if len(even_list[i:]) == 0:
            master_list.append(odd_list[i])
            break
        master_list.append(odd_list[i])
        master_list.append(even_list[i])

    for item in master_list: 
        new_row = {"Rank": int(item[0]), "Name": item[1], "Age":item[3], "Club":item[2], "Matches":item[4], "Goals":item[5]}
        df_top_scorer.loc[len(df_top_scorer)] = new_row

def get_league_table(league_name):
    df = pd.DataFrame(columns = ['Season_End_Year','Team', 'Rank', 'MP', 'W', 'D', 'L', 'GD', 'Pts'])
    league_code = Leagues[league_name]
    url = f'https://www.transfermarkt.com/bundesliga/tabelle/wettbewerb/{league_code}?saison_id='
    get_table(url, df)
    csv_path = f'{league_name}-league-tables.csv'
    df.to_csv(csv_path, index = False)

get_league_table("bundesliga")
get_topscorer("23/24","Top 5 leagues", "All nationalities", "All age groups","All positions","All positions", 5)
#refer to url_data.py for all the options
