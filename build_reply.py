# ------------------------------------------------------------------------
# This file contains two methods, both dedicated to building a reply string.
# The more important method, build_reply, takes a mention string, that
# another Twitter user posted to the Luka bot's account (using the '@').
# Depending on what the mention contains, a reply is built.  The other method
# is used by the bigger method in the case the mention contains '#stats'.  Then
# a special string is built by the add_full_stats_to_reply() method.
#
# author: Ryan Hood
# email: ryanchristopherhood@gmail.com
# ------------------------------------------------------------------------

import stats_scraping

def build_reply(mention):
    # We start with an empty reply string.
    reply = ""

    # If the mention contains '#stats', then we construct a special string by calling the other method.
    if '#stats' in mention.full_text.lower():

        # And we add it to our reply.
        reply += add_full_stats_to_reply(reply)

    # If it doesn't, then the mention must be requesting more specialized stats.  So we go through all cases.
    else:
        # We will explain one entry.  The rest are similar.
        # We first check for '#games' and '#seasongames'.  These both produce the same reply: the number
        # of games played in the current season.  Notice that case is ignored.
        if '#games' in mention.full_text.lower() or '#seasongames' in mention.full_text.lower():
            # We build the reply.
            reply += "Luka has played "
            # We need to get the relevant stat by scraping ESPN.
            reply += str(stats_scraping.get_stats()['season_games'])
            reply += " games this season.\n"
        # The other option is '#careergames'.  This just reports the career games rather than the season games.
        if '#careergames' in mention.full_text.lower():
            reply += "Luka has played "
            reply += str(stats_scraping.get_stats()['career_games'])
            reply += " games in his NBA career.\n"
        # The rest of the stats work identically.
        if '#pointspergame' in mention.full_text.lower() or '#seasonpointspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['season_pts_per_game'])
            reply += " points per game this season.\n"
        if '#careerpointspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['career_pts_per_game'])
            reply += " points per game over his career.\n"
        if '#reboundspergame' in mention.full_text.lower() or '#seasonreboundspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['season_rbs_per_game'])
            reply += " rebounds per game this season.\n"
        if '#careerreboundspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['career_rbs_per_game'])
            reply += " rebounds per game over his NBA career.\n"
        if '#assistspergame' in mention.full_text.lower() or '#seasonassistspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['season_ast_per_game'])
            reply += " assists per game this season.\n"
        if '#careerassistspergame' in mention.full_text.lower():
            reply += "Luka is averaging "
            reply += str(stats_scraping.get_stats()['career_ast_per_game'])
            reply += " assists per game over his NBA career.\n"
        if '#fieldgoal' in mention.full_text.lower() or '#seasonfieldgoal' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['season_fg_percent'])
            reply += "% from the field this season.\n"
        if '#careerfieldgoal' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['career_fg_percent'])
            reply += "% from the field over his NBA career.\n"
        if '#3pt' in mention.full_text.lower() or '#season3pt' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['season_3pt_percent'])
            reply += "% from three this season.\n"
        if '#career3pt' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['career_3pt_percent'])
            reply += "% from three over his NBA career.\n"
        if '#freethrow' in mention.full_text.lower() or '#seasonfreethrow' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['season_ft_percent'])
            reply += "% from the free throw line this season.\n"
        if '#careerfreethrow' in mention.full_text.lower():
            reply += "Luka is shooting "
            reply += str(stats_scraping.get_stats()['career_ft_percent'])
            reply += "% from the free throw line over his NBA career.\n"
        if '#efg' in mention.full_text.lower() or '#seasonefg' in mention.full_text.lower():
            reply += "Luka's effective field goal percent is "
            reply += str(stats_scraping.get_stats()['season_efg_percent'])
            reply += "% this season.\n"
        if '#careerefg' in mention.full_text.lower():
            reply += "Luka's effective field goal percent is "
            reply += str(stats_scraping.get_stats()['career_efg_percent'])
            reply += "% over his NBA career.\n"
        if '#per' in mention.full_text.lower() or '#seasonper' in mention.full_text.lower():
            reply += "Luka's PER is "
            reply += str(stats_scraping.get_stats()['season_per'])
            reply += " this season.\n"
        if '#careerper' in mention.full_text.lower():
            reply += "Luka's PER is "
            reply += str(stats_scraping.get_stats()['career_per'])
            reply += " over his NBA career.\n"
        if '#winshares' in mention.full_text.lower() or '#seasonwinshares' in mention.full_text.lower():
            reply += "Luka has "
            reply += str(stats_scraping.get_stats()['season_win_shares'])
            reply += " win shares this season.\n"
        if '#careerwinshares' in mention.full_text.lower():
            reply += "Luka has "
            reply += str(stats_scraping.get_stats()['career_win_shares'])
            reply += " win shares over his career.\n"
    return reply

def add_full_stats_to_reply(reply):
    # We simply build a fairly simple, all around stat-line consisting of Luka's
    # points, rebounds, and assists averages for the season.
    reply += "Luka is averaging "
    reply += str(stats_scraping.get_stats()['season_pts_per_game'])
    reply += " PPG, "
    reply += str(stats_scraping.get_stats()['season_rbs_per_game'])
    reply += " RPG, and "
    reply += str(stats_scraping.get_stats()['season_ast_per_game'])
    reply += " APG this season."
    return reply
