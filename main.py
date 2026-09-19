from fastapi import FastAPI
import sqlite3

app = FastAPI()

# 1. Create a database table when the app starts
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, skill TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"message": "Elankadhir's First API is Live!"}

# 2. An endpoint to INSERT data into the database
@app.post("/add-user/")
def add_user(name: str, skill: str):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, skill) VALUES (?, ?)", (name, skill))
    conn.commit()
    conn.close()
    return {"message": f"Added {name} with skill: {skill}"}

# 3. An endpoint to SELECT and return data from the database
@app.get("/users/")
def get_users():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"database_records": users}