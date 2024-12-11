from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Date, String, Float
from db import engine 

Base = declarative_base()

# Define the gelen;_yabanci_ziyaretci table
class gelen_yabanci_ziyaretci(Base):
    __tablename__ = 'gelen_yabanci_ziyaretci'
    __table_args__ = {'schema': 'turizm'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    tarih = Column(Date, nullable=True)
    ist_tr = Column(String, nullable=True)
    ziyaretci_sayisi = Column(Float, nullable=True)

# Create table in the database
Base.metadata.create_all(engine)