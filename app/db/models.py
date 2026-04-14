from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    criticality = Column(String, nullable=False)
