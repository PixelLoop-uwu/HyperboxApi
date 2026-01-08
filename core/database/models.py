from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Text
import uuid


Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  discord_id = Column(String, unique=True, nullable=True)
  minecraft_username = Column(String, unique=True, nullable=False)
  uid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  password_hash = Column(String, nullable=False)
  assets_tokens = Column(Text, default="[]")
  creation_date = Column(DateTime, default=datetime.utcnow)