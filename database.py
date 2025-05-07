import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI

app = FastAPI()

# Carrega as variáveis do arquivo .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cria o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"mensagem": "API do Canil está rodando!"}
