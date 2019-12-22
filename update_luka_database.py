# ------------------------------------------------------------------------
# This file contains a method which updates the Luka database that we are
# maintaining.
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
    #lg = last game values from web scraping
    lg_points = str(game_scraping.get_game_stats()["points"])
    lg_rebounds = str(game_scraping.get_game_stats()["rebounds"])
    lg_assists = str(game_scraping.get_game_stats()["assists"])
    lg_field_goals = game_scraping.get_game_stats()["field_goals"] # no str conversion since it already is a string
    lg_minutes_played = str(game_scraping.get_game_stats()["minutes_played"])
    lg_fg_percent = str(game_scraping.get_game_stats()["fg_percent"])
    lg_three_pt_field_goals = game_scraping.get_game_stats()["three_pt_field_goals"] # no str conversion since it already is a string
    lg_three_pt_percent = str(game_scraping.get_game_stats()["three_pt_percent"])
    lg_free_throws = game_scraping.get_game_stats()["free_throws"] # no str conversion since it already is a string
    lg_free_throw_percent = str(game_scraping.get_game_stats()["free_throw_percent"])
    lg_blocks = str(game_scraping.get_game_stats()["blocks"])
    lg_steals = str(game_scraping.get_game_stats()["steals"])
    lg_fouls = str(game_scraping.get_game_stats()["fouls"])
    lg_turnovers = str(game_scraping.get_game_stats()["turnovers"])
    lg_opponent = game_scraping.get_game_stats()["opponent"] # no str conversion since it already is a string
    lg_outcome = game_scraping.get_game_stats()["outcome"] # no str conversion since it already is a string

    # If any of the two values are different, then a new game must have occured.
    if ((db_points != lg_points) or (db_rebounds != lg_rebounds) or (db_assists != lg_assists) or (db_field_goals != lg_field_goals) or (db_minutes_played != lg_minutes_played)
        or (db_fg_percent != lg_fg_percent) or (db_three_pt_field_goals != lg_three_pt_field_goals) or (db_three_pt_percent != lg_three_pt_percent) or
        (db_free_throws != lg_free_throws) or (db_free_throw_percent != lg_free_throw_percent) or (db_blocks != lg_blocks) or (db_steals != lg_steals) or (db_fouls != lg_fouls) or
        (db_turnovers != lg_turnovers) or (db_opponent != lg_opponent) or (db_outcome != lg_outcome)):

        # Report that a new game occured.
        print("New Game Occured...Updating Luka Database.")

        # Create a new entry using the lg values.  Notice that 'game_number' is actually just incremented by 1 over the previous db value.
        new_entry_dict = {'points': game_scraping.get_game_stats()['points'], 'rebounds': game_scraping.get_game_stats()['rebounds'], 'assists': game_scraping.get_game_stats()['assists'], 'field_goals': game_scraping.get_game_stats()['field_goals'], 'minutes_played': game_scraping.get_game_stats()['minutes_played'], 'fg_percent': game_scraping.get_game_stats()['fg_percent'], 'three_pt_field_goals': game_scraping.get_game_stats()['three_pt_field_goals'], 'three_pt_percent': game_scraping.get_game_stats()['three_pt_percent'], 'free_throws': game_scraping.get_game_stats()['free_throws'], 'free_throw_percent': game_scraping.get_game_stats()['free_throw_percent'], 'blocks': game_scraping.get_game_stats()['blocks'], 'steals': game_scraping.get_game_stats()['steals'], 'fouls': game_scraping.get_game_stats()['fouls'], 'turnovers': game_scraping.get_game_stats()['turnovers'], 'opponent': game_scraping.get_game_stats()['opponent'], 'outcome': game_scraping.get_game_stats()['outcome'], 'game_number': db_game_number + 1}

        # Add the new entry to the Data Frame.
        modified_df = df.append(new_entry_dict, ignore_index=True)

        # Write the new Data Frame to the same CSV file.
        modified_df.to_csv(r"C:\Users\User\Data Science Projects\twitter_bots\luka-stats-2019-2020.csv", index=None, header=True)
