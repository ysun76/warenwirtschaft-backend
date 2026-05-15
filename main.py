# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # 用于接收前端传来的 JSON 数据

app = FastAPI()

# Liste der erlaubten Origins (Frontend-URLs)
origins = [
    "http://localhost:5173",            # Lokaler Vite Dev Server
    "https://meinshop.pages.dev",       # Cloudflare Pages Production
    "https://mein-custom-domain.com",   # Eigene Domain (falls vorhanden)
    "https://warenwirtschaft-final.pages.dev"  # 新增：你当前最新的 Cloudflare 前端域名
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Welche Origins sind erlaubt?
    allow_credentials=True,            # Cookies/Auth-Headers erlauben?
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# 临时内存数据库，用于存放你注册的账号
users_db = {}

# 定义前端登录/注册时传过来的数据格式
class UserLogin(BaseModel):
    username: str
    password: str

# 1. 新增注册接口：方便你直接去 /docs 页面注册账号
@app.post("/api/register")
async def register(user: UserLogin):
    users_db[user.username] = user.password
    return {"message": "Erfolgreich registriert", "username": user.username}

# 2. 新增登录接口：供前端表单提交时调用
@app.post("/api/auth/token")
async def login(user: UserLogin):
    # 验证账号是否存在且密码是否正确
    if user.username in users_db and users_db[user.username] == user.password:
        # 返回前端需要的 token 和用户名（模拟标准的 JWT 响应）
        return {
            "token": "fake-jwt-token-for-assignment",
            "username": user.username
        }
    return {"detail": "Ungültige Anmeldedaten"}, 401

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