# ------------------------------------------------------------------------
# This file scrapes Luka Doncic's Basketball Reference page for his season and career stats.
# This is the same idea but different content from the game_scraping.py file
#
# author: Ryan Hood
# email: ryanchristopherhood@gmail.com
# ------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from csv import writer

def get_stats():
    # First, a response is formed, and a BeautifulSoup object created.
    response = requests.get('https://www.basketball-reference.com/players/d/doncilu01.html#all_stats-nba-com')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Using 'class_ = 'poptip'' gets us where we need to be in the HTML code.
    posts = soup.find_all(class_ = 'poptip')

    # We use the find_next_sibling() method to move through the HTML and the get_text() method
    # to only record the numerical values (not the HTML tags).
    season_games = posts[1].find_next_sibling().get_text()
    career_games = posts[1].find_next_sibling().find_next_sibling().get_text()
    season_pts_per_game = posts[2].find_next_sibling().get_text()
    career_pts_per_game = posts[2].find_next_sibling().find_next_sibling().get_text()
    season_rbs_per_game = posts[3].find_next_sibling().get_text()
    career_rbs_per_game = posts[3].find_next_sibling().find_next_sibling().get_text()
    season_ast_per_game = posts[4].find_next_sibling().get_text()
    career_ast_per_game = posts[4].find_next_sibling().find_next_sibling().get_text()
    season_fg_percent = posts[5].find_next_sibling().get_text()
    career_fg_percent = posts[5].find_next_sibling().find_next_sibling().get_text()
    season_3pt_percent = posts[6].find_next_sibling().get_text()
    career_3pt_percent = posts[6].find_next_sibling().find_next_sibling().get_text()
    season_ft_percent = posts[7].find_next_sibling().get_text()
    career_ft_percent = posts[7].find_next_sibling().find_next_sibling().get_text()
    season_efg_percent = posts[8].find_next_sibling().get_text()
    career_efg_percent = posts[8].find_next_sibling().find_next_sibling().get_text()
    season_per = posts[9].find_next_sibling().get_text()
    career_per = posts[9].find_next_sibling().find_next_sibling().get_text()
    season_win_shares = posts[10].find_next_sibling().get_text()
    career_win_shares = posts[10].find_next_sibling().find_next_sibling().get_text()

    # USing all of the vlaues just obtained, a stats_dict is formed and returned.
    stats_dict = {'season_games': season_games , 'career_games': career_games , 'season_pts_per_game': season_pts_per_game , 'career_pts_per_game': career_pts_per_game ,
                    'season_rbs_per_game': season_rbs_per_game , 'career_rbs_per_game': career_rbs_per_game , 'season_ast_per_game': season_ast_per_game , 'career_ast_per_game': career_ast_per_game ,
                    'season_fg_percent': season_fg_percent , 'career_fg_percent': career_fg_percent , 'season_3pt_percent': season_3pt_percent , 'career_3pt_percent': career_3pt_percent ,
                    'season_ft_percent': season_ft_percent , 'career_ft_percent': career_ft_percent , 'season_efg_percent': season_efg_percent ,
                    'career_efg_percent': career_efg_percent , 'season_per': season_per , 'career_per': career_per , 'season_win_shares': season_win_shares ,
                    'career_win_shares': career_win_shares}
    return stats_dict
