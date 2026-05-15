# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Liste der erlaubten Origins (Frontend-URLs)
origins = [
    "http://localhost:5173",            # Lokaler Vite Dev Server
    "https://meinshop.pages.dev",       # Cloudflare Pages Production
    "https://mein-custom-domain.com",   # Eigene Domain (falls vorhanden)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Welche Origins sind erlaubt?
    allow_credentials=True,            # Cookies/Auth-Headers erlauben?
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

produkte_db = [
    {
        "id": 1, 
        "name": "Apfel Gala", 
        "preis": 2.99, 
        "kategorie": "Obst", 
        "istVerfuegbar": True
    },
    {
        "id": 2, 
        "name": "Vollmilch 3.5%", 
        "preis": 1.49, 
        "kategorie": "Milchprodukte", 
        "istVerfuegbar": True
    },
    {
        "id": 3, 
        "name": "Bio-Eier (10er)", 
        "preis": 3.29, 
        "kategorie": "Eier", 
        "istVerfuegbar": False
    }
]

@app.get("/api/products")
async def get_products():
    return produkte_db