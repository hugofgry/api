from fastapi import FastAPI
import uvicorn
import sqlite3
from sqlite3 import connect

conn = sqlite3.connect('scrap_game.db')
c = conn.cursor()
app = FastAPI()

@app.get("/games")
async def one_game ():
    c.execute("SELECT title, type, release_date,platform, publisher  FROM games JOIN release_details ON games.id = release_details.game_id JOIN games_details ON games.id = games_details.game_id;")
    game = c.fetchall()
    conn.commit()
    return game

@app.get("/games/count")
async def count_platform():
    c.execute("SELECT Plateforme, COUNT(Plateforme) FROM games GROUP BY Plateforme;")
    count = c.fetchall()
    conn.commit()
    return count


    SELECT title, type, release_date,platform, publisher  FROM games JOIN release_details ON games.id = release_details.game_id JOIN games_details ON games.id = games_details.game_id;
