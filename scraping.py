from requests import get
from bs4 import BeautifulSoup
import csv
import pandas as pd

BASE_URL = "https://www.mlb.com"
URL = "https://www.mlb.com/whitesox/stats/"

def get_rows(page):
    rows = page.find_all('tr')
    return rows

def get_player_info(row):
    name = row.find('a')['aria-label']
    position = row.find('div', class_="position-28TbwVOg").text 
    stats = row.find_all('td', scope="row")
    team = stats[0].text 
    games_played = stats[1].text
    at_bats = stats[2].text 
    runs = stats[3].text 
    hits = stats[4].text 
    doubles = stats[5].text 
    triples = stats[6].text
    home_runs = stats[7].text
    rbis = stats[8].text
    walks = stats[9].text 
    strikeouts = stats[10].text 
    stolen_bases = stats[11].text 
    caught_stealing = stats[12].text 
    batting_average = stats[13].text 
    on_base_percentage = stats[14].text 
    slugging_percentage = stats[15].text
    on_base_plus_slugging = stats[16].text

    return name, position, team, games_played, at_bats, runs, hits, doubles, triples, home_runs, rbis, walks, strikeouts, stolen_bases, caught_stealing, batting_average, on_base_percentage, slugging_percentage, on_base_plus_slugging


def test_extractors():
    page = BeautifulSoup(get(URL).text, features="html.parser")
    rows = get_rows(page)
    assert len(rows) == 25, "There are 25 rows"
    assert "PLAYER" in rows[0].text, "The first row includes PLAYER"

    first_player = rows[1]
    first_player_info = get_player_info(first_player)
    nameCheck = first_player_info[0]
    abs = first_player_info[4]
    ts = first_player_info[8]
    obps = first_player_info[18]
    assert nameCheck == "Jose Abreu"
    assert abs == "234"
    assert ts == "1"
    assert obps == ".792"

if __name__ == "__main__":
    page_html = get(URL).text
    page = BeautifulSoup(page_html, features="html.parser")
    rows = get_rows(page)
    stats_string = ""
    with open ('stats.csv', 'a') as f:
        f1 = csv.writer(f)
        for i, row in enumerate(rows):
            if (i == 0):
                i = i + 1
            player = rows[i]
            player_info = get_player_info(player)
            nameReturn = player_info[0]
            positionReturn = player_info[1]
            teamReturn = player_info[2]
            gp = player_info[3]
            ab = player_info[4]
            r = player_info[5]
            h = player_info[6]
            d = player_info[7]
            t = player_info[8]
            hr = player_info[9]
            rbi = player_info[10]
            w = player_info[11]
            so = player_info[12]
            sb = player_info[13]
            cs = player_info[14]
            ba = player_info[15]
            obp = player_info[16]
            sp = player_info[17]
            obs = player_info[18]
            playerStats = {'Name' : [nameReturn], 'Position' : [positionReturn], 'Team' : [teamReturn], 'Games played' : [gp], 'At bats' : [ab], 'Runs' : [r], 'Hits' : [h], 'Doubles' : [d], 'Triples' : [t], 'Home runs' : [hr], 'Runs batted in' : [rbi], 'Walks' : [w], 'Strikeouts' : [so], 'Stolen bases' : [sb], 'Caught stealing' : [cs], 'Batting average' : [ba], 'On-base percentage' : [obp], 'Slugging percentage' : [sp], 'On-base plus slugging' : [obs]}
            stats_string = str(stats_string) + str(playerStats) + str('\n')
        df = pd.DataFrame([stats_string])
        df.to_csv('stats.csv')

    breakpoint()

