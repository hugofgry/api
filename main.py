from fastapi import FastAPI
import uvicorn
import sqlite3

conn = sqlite3.connect('scrap_game.db')
c = conn.cursor()
app = FastAPI()

@app.get("/games")
async def one_game ():
    c.execute("SELECT * FROM games;")
    game = c.fetchall()
    conn.commit()
    return game

@app.get("/games/count")
async def count_platform():
    c.execute("SELECT Plateforme, COUNT(Plateforme) FROM games GROUP BY Plateforme;")
    count = c.fetchall()
    conn.commit()
    return count