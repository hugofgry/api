from fastapi import FastAPI
import sqlite3
import uvicorn
from sqlite3 import connect
from bs4 import BeautifulSoup
import urllib.request
import json
import sys
import pandas as pd
import os
from fastapi.responses import JSONResponse

app = FastAPI()
# Connection a la base sqlite
conn = sqlite3.connect('scrap_game.db')
c = conn.cursor()
# Selection de la base de donnée
# Selection de la collection == SQL Table




@app.get("/games")
async def all_game ():
    c.execute("SELECT title, type, release_date,platform,price, publisher FROM games JOIN release_details ON games.id = release_details.game_id JOIN games_details ON games.id = games_details.game_id;")
    game = c.fetchall()
    conn.commit()
    return game

@app.get("/games/count")
async def count_platform():
    df = pd.read_sql_query("SELECT platform, COUNT(platform) FROM release_details GROUP BY platform;", conn)
    df = df.rename(columns={'COUNT(platform)': 'pourcent', "platform" : "name"})
    d = df.to_dict('records')
    headers = {"Access-Control-Allow-Origin":"*"}
    conn.commit()
    return JSONResponse(content=d, headers=headers)



@app.get("/games/type")
async def diferents_types():
    df = pd.read_sql_query("SELECT type, COUNT(type) FROM games GROUP BY type;", conn)
    df = df.rename(columns={'COUNT(type)': 'nombres', "type" : "genre"})
    d = df.to_dict('records')
    headers = {"Access-Control-Allow-Origin":"*"}
    conn.commit()
    return JSONResponse(content=d, headers=headers)

@app.get("/admin2468/start_scrap")
async def start_scrapper():

  inc = 0
  nomdomaine = 'https://www.gamecash.fr'
  urlpage = 'https://www.gamecash.fr/prochaines-sorties.html?o=t&s=a'
  links = []

  print('Lancement du scraper ...')
  os.remove("scrap_game.db")
  conn = connect('scrap_game.db')
  curs = conn.cursor()

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  def create_table():
    curs.execute('''CREATE TABLE IF NOT EXISTS games (
    id  INT,
    title TEXT,
    type TEXT,
    release_date TEXT,
    price TEXT)'''
    );
    curs.execute('''CREATE TABLE IF NOT EXISTS release_details (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT,
    platform TEXT)'''
    );
    curs.execute('''CREATE TABLE IF NOT EXISTS games_details (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT,
    publisher TEXT,
    description TEXT)'''
    );
    conn.commit()

  class Jeux :
    game_id = 0
    titre_precedent = ""

    def __init__(self, titre:str, genre:str, prix:str,plateforme:str, date_de_sortie:str,editeur:str,description:str) :
      self.titre = titre
      self.genre = genre
      self.prix = prix
      self.plateforme = plateforme
      self.date_de_sortie = date_de_sortie
      self.editeur = editeur
      self.description = description

    def insert_values_db(self, titre:str, genre:str, prix:str,plateforme:str, date_de_sortie:str,editeur:str,description:str) :
      if Jeux.titre_precedent != self.titre :
        Jeux.game_id += 1
        curs.execute("INSERT INTO games (id, title, type, price, release_date) VALUES (?, ?, ?, ?, ?);", (Jeux.game_id, self.titre, self.genre, self.prix, self.date_de_sortie))
        curs.execute("INSERT INTO games_details (game_id, publisher, description) VALUES (?, ?, ?);", (Jeux.game_id, self.editeur, self.description))
      curs.execute("INSERT INTO release_details (game_id, platform) VALUES (?, ?);", (Jeux.game_id, self.plateforme))
      conn.commit()
      Jeux.titre_precedent = self.titre

    def console_logs(self, titre:str, genre:str, prix:str,plateforme:str, date_de_sortie:str,editeur:str,description:str) :
      print("Game_ID >",Jeux.game_id,"\nTitre >",self.titre,"\nGenre >",self.genre,"\nPrix >",self.prix,"\nPlateforme >",self.plateforme,"\nDate de sortie >",self.date_de_sortie,"\nEditeur >",self.editeur,"\nDescription >",self.description)

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  create_table()

  #PARSER RECUPERATION LINKS
  page = urllib.request.urlopen(urlpage)
  soup = BeautifulSoup(page, 'html.parser')

  # On cherche et on append les liens
  table = soup.find('table', attrs={'class': 'table'})
  results = table.find_all('tr')
  for result in results:
    data = result.find_all('td')
    if len(data) == 0:
      continue
    data1 = data[1]
    a = data1.find('a')
    href = a['href']
    links.append(nomdomaine + href)

  print("Nombre d'URL stockées dans notre liste >",len(links))

  for link in links :
    #PARSER SUR CHAQUE PAGE
    pagelink = urllib.request.urlopen(link)
    soup2 = BeautifulSoup(pagelink, 'html.parser')

    inc += 1
    titre = "Null"
    prix = "Null"
    plateforme = "Null"
    genre = "Null"
    editeur = "Null"
    date_de_sortie = "Null"
    description = "Null"

    print("-----------------------------------------------------------------------------------\n>>>>>>> Link",inc,"/",len(links)," >",link,"\n")

    #On cherche le prix
    scrap_price = soup2.find('meta', attrs={'itemprop': 'price'})
    prix = scrap_price['content']

    #On cherche le titre
    scrap_title = soup2.find('h1', attrs={'itemprop': 'name'})
    titre = scrap_title.text
    titre = titre.strip()

    #On cherche la desc
    scrap_desc = soup2.find('div', attrs={'itemprop': 'description'})
    try :
      description = scrap_desc.text
      description = description.strip()
    except :
      description = "Null"
      pass

    #On cherche les infos pas importantes (Editeur ...)
    table2 = soup2.find_all('ul')
    table2_3 = table2[3]
    i = -1
    for ahah in table2_3 :
      i += 1
      if len(ahah) == 4 :
        sPaN = ahah.find('span', attrs={'class': 'value'})
        sPaN = sPaN.text
      if i == 0 :
        plateforme = sPaN
      elif i == 2:
        genre = sPaN
      elif i == 4 :
        editeur = sPaN
      elif i == 6 :
        if len(sPaN) == 10 :
          date_de_sortie = sPaN
      elif i == 10 :
        if len(sPaN) == 10 :
          date_de_sortie = sPaN
      elif i == 12 :
        date_de_sortie = sPaN
    if len(date_de_sortie) != 10 :
      date_de_sortie = "Null"

    df2 = pd.read_sql_query("SELECT title,release_date FROM games ;", conn)
    df2['release_date'] = pd.to_datetime(df2['release_date'], format='%d/%m/%Y', errors='coerce')

    jeux_objet = Jeux(titre,genre,prix,plateforme,date_de_sortie,editeur,description)
    jeux_objet.insert_values_db(titre,genre,prix,plateforme,date_de_sortie,editeur,description)
    jeux_objet.console_logs(titre,genre,prix,plateforme,date_de_sortie,editeur,description)
  conn.close()

  return {'response' : 'ok'}



#     return {"student_id": student_id}


@app.get("/games/count/publisher")
async def get_count_publisher():
  df = pd.read_sql_query("SELECT publisher, COUNT(publisher) FROM games_details GROUP BY publisher;", conn)
  df = df.rename(columns={'COUNT(publisher)': 'nombre', "publisher" : "name"})
  d = df.to_dict('records')
  headers = {"Access-Control-Allow-Origin":"*"}
  conn.commit()
  return JSONResponse(content=d, headers=headers)
# @app.post("/students")
# async def create_student(student: Student):
#     student_id = str(COLLECTION_STUDENTS.insert_one(student.dict()).inserted_id)
#     # TODO : Envoyer un mail de confirmation
#     return {"student_id": student_id}


# @app.put("/students")
# async def update_student():
#     return "Not yet implemented"


#@app.delete("/students/id/{id}")
#async def delete_student_by_id(id):
#    return {"id": id}


#@app.delete("/students/name/{lastname}")
#async def delete_student_by_name(lastname):
#    return {"lastname": lastname}
