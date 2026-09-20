from fastapi import FastAPI
import sqlite3
import os
from dotenv import load_dotenv
from google import genai

# Load hidden variables from the .env file
load_dotenv()

# Retrieve the key securely
secure_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=secure_api_key)

app = FastAPI()

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, skill TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"status": "SUCCESS! Backend is running.", "developer": "Elankadhir Agilan"}

@app.post("/add-user/")
def add_user(name: str, skill: str):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, skill) VALUES (?, ?)", (name, skill))
    conn.commit()
    conn.close()
    return {"message": f"Successfully stored {name} into SQL database."}

@app.get("/users/")
def get_users():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    conn.close()
    return {"total_records": len(records), "data": records}

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": f"Deleted user with ID: {user_id}"}

# DIAGNOSTIC: Ask Google exactly what models your key can access
@app.get("/models/")
def check_google_models():
    try:
        allowed_models = []
        for m in client.models.list():
            allowed_models.append(m.name)
        return {"your_available_models": allowed_models}
    except Exception as e:
        return {"error": f"Could not fetch models: {str(e)}"}

@app.post("/ask-ai/")
def ask_ai(prompt: str, model_name: str = "gemini-3.6-flash"):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return {"prompt": prompt, "model_used": model_name, "ai_response": response.text}
    except Exception as e:
        return {"error": f"Google AI Engine failed: {str(e)}"}