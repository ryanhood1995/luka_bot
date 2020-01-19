# ------------------------------------------------------------------------
# This file contains a method which updates the Luka dataset that we are
# maintaining.  Excel is unfriendly with entries "12-15" interpreting them
# as dates.  To prevent this from happening, a helper function that turns
# input like "12-15" into "12--15" is employed for those cells.
#
# author: Ryan Hood
# email: ryanchristopherhood@gmail.com
# ------------------------------------------------------------------------

import game_scraping
import pandas as pd
import numpy as np

def update_database():
    # First, we read in the current Data Frame
    df = pd.read_csv(r"C:\Users\User\Data Science Projects\twitter_bots\luka-stats-2019-2020.csv", encoding="utf-8-sig")
    # df = df.dropna(axis='rows')

    # Now, we use the Data Frame just constructed to get the last game's stats.
    # These are, of course, at index -1.
    # db = databse values
    db_points = str(df['points'].iloc[-1])
    db_rebounds = str(df['rebounds'].iloc[-1])
    db_assists = str(df['assists'].iloc[-1])
    db_field_goals = df['field_goals'].iloc[-1] # no str conversion since it already is a string
    db_minutes_played = str(df['minutes_played'].iloc[-1])
    db_fg_percent = str(df['fg_percent'].iloc[-1])
    db_three_pt_field_goals = df['three_pt_field_goals'].iloc[-1] # no str conversion since it already is a string
    db_three_pt_percent = str(df['three_pt_percent'].iloc[-1])
    db_free_throws = df['free_throws'].iloc[-1] # no str conversion since it already is a string
    db_free_throw_percent = str(df['free_throw_percent'].iloc[-1])
    db_blocks = str(df['blocks'].iloc[-1])
    db_steals = str(df['steals'].iloc[-1])
    db_fouls = str(df['fouls'].iloc[-1])
    db_turnovers = str(df['turnovers'].iloc[-1])
    db_opponent = df['opponent'].iloc[-1] # no str conversion since it already is a string
    db_outcome = df['outcome'].iloc[-1] # no str conversion since it already is a string
    db_game_number = df['game_number'].iloc[-1]

    # Now, we get the same stats from the ESPN website
    # lg = last game values from web scraping
    newest_game_dict = game_scraping.get_game_stats()

    lg_points = str(newest_game_dict["points"])
    lg_rebounds = str(newest_game_dict["rebounds"])
    lg_assists = str(newest_game_dict["assists"])
    lg_field_goals = newest_game_dict["field_goals"] # no str conversion since it already is a string
    lg_minutes_played = str(newest_game_dict["minutes_played"])
    lg_fg_percent = str(newest_game_dict["fg_percent"])
    lg_three_pt_field_goals = newest_game_dict["three_pt_field_goals"] # no str conversion since it already is a string
    lg_three_pt_percent = str(newest_game_dict["three_pt_percent"])
    lg_free_throws = newest_game_dict["free_throws"] # no str conversion since it already is a string
    lg_free_throw_percent = str(newest_game_dict["free_throw_percent"])
    lg_blocks = str(newest_game_dict["blocks"])
    lg_steals = str(newest_game_dict["steals"])
    lg_fouls = str(newest_game_dict["fouls"])
    lg_turnovers = str(newest_game_dict["turnovers"])
    lg_opponent = newest_game_dict["opponent"] # no str conversion since it already is a string
    lg_outcome = newest_game_dict["outcome"] # no str conversion since it already is a string

    # If any of the two values are different, then a new game must have occured.
    if ((db_points != lg_points) or (db_rebounds != lg_rebounds) or (db_assists != lg_assists) or (db_field_goals != lg_field_goals) or (db_minutes_played != lg_minutes_played)
        or (db_fg_percent != lg_fg_percent) or (db_three_pt_field_goals != lg_three_pt_field_goals) or (db_three_pt_percent != lg_three_pt_percent) or
        (db_free_throws != lg_free_throws) or (db_free_throw_percent != lg_free_throw_percent) or (db_blocks != lg_blocks) or (db_steals != lg_steals) or (db_fouls != lg_fouls) or
        (db_turnovers != lg_turnovers) or (db_opponent != lg_opponent) or (db_outcome != lg_outcome)):

        # Report that a new game occured.
        print("New Game Occured...Updating Luka Database.")

        # Create a new entry using the lg values.  Notice that 'game_number' is actually just incremented by 1 over the previous db value.
        new_entry_dict = {'points': lg_points, 'rebounds': lg_rebounds, 'assists': lg_assists, 'field_goals': convertToTwoDashes(lg_field_goals), 'minutes_played': lg_minutes_played, 'fg_percent': lg_fg_percent, 'three_pt_field_goals': convertToTwoDashes(lg_three_pt_field_goals), 'three_pt_percent': lg_three_pt_percent, 'free_throws': convertToTwoDashes(lg_free_throws), 'free_throw_percent': lg_free_throw_percent
        , 'blocks': lg_blocks, 'steals': lg_steals, 'fouls': lg_fouls, 'turnovers': lg_turnovers, 'opponent': lg_opponent, 'outcome': lg_outcome, 'game_number': db_game_number + 1}

        # Add the new entry to the Data Frame.
        modified_df = df.append(new_entry_dict, ignore_index=True)

        # Write the new Data Frame to the same CSV file.
        modified_df.to_csv(r"C:\Users\User\Data Science Projects\twitter_bots\luka-stats-2019-2020.csv", index=None, header=True)


def convertToTwoDashes(one_dash_string):
    # First find the index of the dash in the one_dash_string
    for i in range(0, len(one_dash_string)-1):
        if (one_dash_string[i] == "-"):
            index = i

    # Now construct the new string in three parts: 1.) Before dash 2.) Two dashes 3.) After dash.
    two_dash_string = one_dash_string[:index]
    two_dash_string = two_dash_string + "--"
    two_dash_string = two_dash_string + one_dash_string[index+1:]

    return two_dash_string
