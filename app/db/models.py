from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    criticality = Column(String, nullable=False)


class AssetRelation(Base):
    __tablename__ = "asset_relations"

    id = Column(Integer, primary_key=True, index=True)
    source_asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    target_asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    relation_type = Column(String, nullable=False)
