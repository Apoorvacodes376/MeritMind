from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class JDHistory(Base):
    __tablename__ = "jd_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_jd = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BiasResult(Base):
    __tablename__ = "bias_results"
    id = Column(Integer, primary_key=True, index=True)
    jd_id = Column(Integer, ForeignKey("jd_history.id"))
    bias_score = Column(Integer)
    bias_matrix = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class RewriteResult(Base):
    __tablename__ = "rewrite_results"
    id = Column(Integer, primary_key=True, index=True)
    jd_id = Column(Integer, ForeignKey("jd_history.id"))
    conservative = Column(Text)
    balanced = Column(Text)
    inclusive = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String)
    input_data = Column(Text)
    output_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)