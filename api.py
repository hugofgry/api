from fastapi import FastAPI
import sqlite3
import uvicorn

app = FastAPI()
# Connection a la base sqlite
conn = sqlite3.connect('scrap_game(1).db')
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
    c.execute("SELECT platform, COUNT(platform) FROM release_details GROUP BY platform;")
    count = c.fetchall()
    conn.commit()
    return count



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
