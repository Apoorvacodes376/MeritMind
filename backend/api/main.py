from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))

app = FastAPI(title="Merit Mind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class JDInput(BaseModel):
    text: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Database tables created successfully")

@app.get("/")
def home():
    return {"message": "Merit Mind Backend is Running ✅"}

@app.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    from auth import register_user
    return register_user(data.name, data.email, data.password, db)

@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    from auth import login_user
    return login_user(data.email, data.password, db)

@app.post("/detect-bias")
async def detect_bias(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Bias detection coming soon"}

@app.post("/rewrite-jd")
async def rewrite_jd(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Job rewriter coming soon"}

@app.post("/counterfactual")
async def counterfactual(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Counterfactual coming soon"}

@app.post("/skill-graph")
async def skill_graph(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Skill graph coming soon"}

@app.post("/fairness-optimizer")
async def fairness_optimizer(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Fairness optimizer coming soon"}

@app.post("/silence-rank")
async def silence_rank(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Silence rank coming soon"}

@app.post("/emotion-blind")
async def emotion_blind(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Emotion blind coming soon"}

@app.post("/bias-simulator")
async def bias_simulator(data: JDInput, db: Session = Depends(get_db)):
    return {"message": "Bias simulator coming soon"}