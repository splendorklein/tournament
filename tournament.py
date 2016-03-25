#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
from contextlib import contextmanager
import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Failed to connect the database!")
"""It's inspired by the last project review to write it this way. Part of the connect and the get_cursor function cited from the reviewer's instruction."""
@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    DB = connect()
    cursor = DB.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        DB.commit()
    finally:
        cursor.close()
        DB.close()


def deleteMatches():
    """Remove all the match records from the database."""

    with get_cursor() as cursor:
        cursor.execute("DELETE FROM matches")
        cursor.execute("DELETE FROM opponentlist")
        cursor.execute("UPDATE players set score = 0, games = 0 ")


def deletePlayers():
    """Remove all the player records from the database."""

    with get_cursor() as cursor:
        cursor.execute("DELETE FROM players")

def countPlayers():
    """Returns the number of players currently registered."""


    

    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(name) as num from players")
        count = cursor.fetchall()[0][0]
        return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    with get_cursor() as cursor:
        cursor.execute("INSERT INTO players (name, score, games) VALUES (%s,%s,%s)",(name,str(0),str(0)))    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    with get_cursor() as cursor:
        cursor.execute("SELECT * from opponent") 
        Players = [(row[3], str(row[0]), row[1], row[2]) for row in cursor.fetchall()]    
        return Players

def reportMatch(winner, loser, round):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    with get_cursor() as cursor:
        cursor.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s)",(str(winner),str(loser)))
        cursor.execute("UPDATE players set score = score + 1, games = games +1 where id = %s" , (str(winner),))
        cursor.execute("UPDATE players set games = games +1 where id = %s" , (str(loser),)) 
        cursor.execute("INSERT INTO opponentlist VALUES (%s,%s,%s)" , (str(winner),str(loser),str(round)))
        cursor.execute("INSERT INTO opponentlist VALUES (%s,%s,%s)" , (str(loser),str(winner),str(round)))
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    Players = playerStandings()
    playerlist=[]
    for i in range(len(Players)/2):
        playerlist.append((Players[i*2][0],Players[i*2][1],Players[i*2+1][0],Players[i*2+1][1]))
    return playerlist

def querytheview():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * from opponent")
    result = c.fetchall()
    DB.close()    
    return result
