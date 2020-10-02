from fastapi import FastAPI
import sqlite3
import uvicorn

app = FastAPI()
# Connection a la base sqlite
connection = sqlite3.connect('scrap_game.db')
c = connection.cursor()
# Selection de la base de donnée
# Selection de la collection == SQL Table




@app.get("/games")
async def get_all_game():
    c.execute("SELECT * FROM games;")
    game = c.fetchall()
    connection.commit()
    return game

@app.get("/camambert_plateforme")
async def plateforme_count():
  c.execute("SELECT Plateforme, COUNT(Plateforme) FROM games GROUP BY Plateforme;")
  co = c.fetchall()
  connection.commit()
  return co

@app.get("/games/name")
async def get_all_names():
    c.execute("SELECT Titre FROM games;")
    game = c.fetchall()
    connection.commit()
    return game


# @app.get("/students/id/{student_id}")
# async def get_student_by_id(student_id):
#     return {"student_id": student_id}


# @app.get("/students/name/{lastname}")
# async def get_student_by_name(lastname):
#   student = COLLECTION_STUDENTS.find_one({"name" : lastname})
#   student["_id"] = str(student["_id"])
#   return student


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
