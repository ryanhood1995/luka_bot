# ------------------------------------------------------------------------
# Uses the BeautifulSoup module to get Luka Doncic's stats for the most
# recently played game.  There are also methods for cleaning up some
# messy output and determining when Luka misses a game.
#
# author: Ryan Hood
# email: ryanchristopherhood@gmail.com
# ------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from csv import writer

def get_game_stats():
    # Response HTML code is gathered from Luka Doncic's page on ESPN.
    response = requests.get('https://www.espn.com/nba/player/gamelog/_/id/3945274/luka-doncic')

    # A BeautifulSoup object is created for the HTML code.
    soup = BeautifulSoup(response.text, 'html.parser')

    # Using 'class_ = 'Table__TD'' gets us the closest to the stats we care about.
    posts = soup.find_all(class_ = 'Table__TD')

    # The below lines gather all of the stats by crawling through the code with the find_next_sibling() method.  At the end, we use the get_text()
    # method to isloate only the numerical value.  The code isn't the prettiest, but it works.
    points = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    rebounds = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    assists = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    field_goals = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    minutes_played = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    fg_percent = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    three_pt_field_goals = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    three_pt_percent = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    free_throws = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    free_throw_percent = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    blocks = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    steals = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    fouls = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()
    turnovers = posts[0].find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text()

    # Due to the nature of the web page, the below strings, must be alterted to remove unwanted aspects.
    messy_opponent_string = posts[0].find_next_sibling().get_text()
    messy_score_string = posts[0].find_next_sibling().find_next_sibling().get_text()

    # We call the below methods to clean up the messy strings.
    opponent = convert_opponent_string(messy_opponent_string)
    outcome = get_outcome(messy_score_string)

    # We generate a game_dict object, which contains all of the values just found.
    game_dict = {'points': points, 'rebounds': rebounds, 'assists': assists, 'field_goals': field_goals, 'minutes_played': minutes_played, 'fg_percent': fg_percent, 'three_pt_field_goals': three_pt_field_goals, 'three_pt_percent': three_pt_percent, 'free_throws': free_throws, 'free_throw_percent': free_throw_percent, 'blocks': blocks, 'steals': steals, 'fouls': fouls, 'turnovers': turnovers, 'opponent': opponent, 'outcome': outcome}
    return game_dict

def convert_opponent_string(messy_string):
    # This method is needed since the above method returns something like "vsMIA" for the opponent string.
    # We would like to remove the "vs" part, so we only have the opponent.
    # There are two main difficulties:
    # 1.) Some games are away games, reported "@MIA" and some games are home games, reported "vsMIA".  So we can't just remove the first 2 characters.
    # 2.) Some opponents have 2 letter abbreviations, such as New Orleans (NO) and some teams have 3 letter abbreviations, such as Miami (MIA)
    # So we just have to be careful to consider all cases and only remove the unwanted parts of the string.
    if (len(messy_string) == 5):
        # Must be home game with 3 letter opponent.
        opponent = messy_string[2:]
    elif (len(messy_string) == 4):
        # Could be away game with 3 letter opponent or home game with 2 letter opponent.
        # Another if needed.
        if ("@" in messy_string):
            opponent = messy_string[1:]
        else:
            opponent = messy_string[2:]
    elif (len(messy_string) == 3):
        # Must be away game with 2 letter opponent.
        opponent = messy_string[1:]
    else:
        # If one of the above conditions does not hold, something terrible occured.
        print("HOUSTON, WE HAVE A PROBLEM.")
    return opponent

def get_outcome(messy_string):
    # The purpose of this method is to turn 'W' or 'L' into 'win' or 'loss' respectively.
    outcome = messy_string[0]
    if (outcome == 'W'):
        return 'win'
    return 'loss'

def luka_is_injured_or_resting():
    # The purpose of this method is to determine if Luka played any minutes.
    # If he didn't he is either resting or injured.
    if (get_game_stats()['minutes_played'] == 0):
        return True
    return False

def game_happened(last_game_stats):
    # This method takes an old occurence of game_stats and re-runs the get_game_stats() method.  If there is disagreement on
    # the points, rebounds, assists, field goals, or minutes played, then there almost certainly was a new game.
    # First, get a dict of the most recent game stats.
    newest_game_dict = get_game_stats()
    if (last_game_stats['points'] == newest_game_dict['points'] and last_game_stats['rebounds'] == newest_game_dict['rebounds'] and last_game_stats['assists'] == newest_game_dict['assists'] and last_game_stats['field_goals'] == newest_game_dict['field_goals'] and last_game_stats['minutes_played'] == newest_game_dict['minutes_played']):
        return False
    return True
