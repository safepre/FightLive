from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Fighter(Base):
    __tablename__ = 'fighters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    full_name = Column(String, nullable=False, unique=True)
    
    fights_as_fighter = relationship("Fight", back_populates="fighter", foreign_keys="Fight.fighter_id")
    fights_as_opponent = relationship("Fight", back_populates="opponent", foreign_keys="Fight.opponent_id")

class Scorecard(Base):
    __tablename__ = 'scorecards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    link = Column(String, nullable=False)
    
    fight = relationship("Fight", back_populates="scorecard", uselist=False)

class Fight(Base):
    __tablename__ = 'fights'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    fighter_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    opponent_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    scorecard_id = Column(Integer, ForeignKey('scorecards.id'), nullable=False)

    fighter = relationship("Fighter", foreign_keys=[fighter_id], back_populates="fights_as_fighter")
    opponent = relationship("Fighter", foreign_keys=[opponent_id], back_populates="fights_as_opponent")
    scorecard = relationship("Scorecard", back_populates="fight")
