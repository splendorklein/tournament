-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players ( name TEXT,
	 				   score integer,
	 				   games integer,
                       id SERIAL primary key );


CREATE TABLE matches ( 
                       winner integer,
                       loser integer );

CREATE TABLE opponentlist (
							playerid integer references players (id),
							opponentid integer references players (id),
							round integer);


CREATE VIEW opponent as select OMW.name, OMW.score, OMW.games, OMW.id, sum(opponents.oscore) as OMWscore
						from (players left join opponentlist on players.id = opponentlist.playerid) as OMW 
						left join players as opponents (oname, oscore, ogames, opid) on OMW.opponentid = opponents.opid 
						group by OMW.id order by OMW.score desc, OMWscore desc;


