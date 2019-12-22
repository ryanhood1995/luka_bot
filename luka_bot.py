# ------------------------------------------------------------------------
# This is the driver file for the program.  It contains various methods
# capable of responding to tweets, posting tweets, and posting visualizations.
# At the bottom, you will find the 'main' part, which executes all of the
# functionality using an ifninite loop which cycles every so often.
#
# author: Ryan Hood
# email: ryanchristopherhood@gmail.com
# ------------------------------------------------------------------------

import tweepy
import time
import stats_scraping
import game_scraping
import build_reply
import twitter_keys
import update_luka_database

CONSUMER_KEY = twitter_keys.CONSUMER_KEY
CONSUMER_SECRET = twitter_keys.CONSUMER_SECRET
ACCESS_KEY = twitter_keys.ACCESS_KEY
ACCESS_SECRET = twitter_keys.ACCESS_SECRET

# This sets up Twitter Authentication using the above keys.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# This is the file name used to store the tweet id of the tweet last responded to by the Bot.
FILE_NAME = 'last_seen_id.txt'

# This simple method reads in the last_seen_id.txt file which contains the tweet id last processed
# by the reply_to_tweets() method.  This method returns that ID.
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# This simple method takes the truly last_seen_id and a file name, and writes that id to that file.
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# This method is responsible for replying to tweets and updating the last_seen_id.
def reply_to_tweets():
    print("Retrieving tweets...")

    # We retrieve the 'last_seen_id'.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    # Starting from the 'last_seen_id', we form a list of all the mentions we recieved.
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    # Now we iterate through all of the mentions.
    for mention in reversed(mentions):
        # Update the 'last_seen_id' to reflect the id we are currently processing.
        last_seen_id = mention.id

        # And then store that new id in the file.
        store_last_seen_id(last_seen_id, FILE_NAME)

        # Build the reply using methods defined in build_reply.py.
        reply = build_reply(mention)

        # Display it to the console for diagnostic purposes.
        print(reply)

        # If there is no reply, then no keywords were in the mention.  In that case, ignore the tweet.
        if  not reply:
            continue
        # else... there were keywords, so we need to reply with our built reply.
        else:
            print("Processing Reply...")

            # We get the screen name and the id from the mention object.  The code below replies.
            api.update_status('@' + mention.user.screen_name +  " " + reply, mention.id)

# This method posts Luka's stat line after every game.
def post_game_stats(current_stats_dict):
    # First we check to see if a game even happened or if Luka played in the game.
    if (game_scraping.game_happened(current_stats_dict) and not game_scraping.luka_is_injured_or_resting()):

        # If a game has occured, we update the data set.
        update_luka_database.update_database()

        # We get the up-to-date stats for the game just played.
        current_stats_dict = game_scraping.get_game_stats()
        print("Reporting new game sats.")

        # And we tweet the most relevant stats (PTS, RBS, AST, FG%, outcome, opponent)
        api.update_status("Luka had " + current_stats_dict['points'] + " PTS, " + current_stats_dict['rebounds'] + " RBS, " + current_stats_dict['assists'] + " AST while shooting " + current_stats_dict['field_goals'] + " from the floor in a " + current_stats_dict['outcome'] + " against " + current_stats_dict['opponent'] + ".")


    # Afterwards, we return the current_stats_dict.
    return current_stats_dict


# --------------------------------------------
# ------------------MAIN----------------------
# --------------------------------------------

# First, get Luka's stats in the latest game played.
current_stats_dict = game_scraping.get_game_stats()
while True:
    # First, reply to mentions.
    reply_to_tweets()

    # Then post game stats, if a new game has been played.
    current_stats_dict = post_game_stats(current_stats_dict)

    # Post visualizations...

    # Sleep for a set amount of seconds.
    time.sleep(15)
