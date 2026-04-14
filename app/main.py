from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.database import engine, SessionLocal
from app.db.models import Base, Asset
from app.db.schemas import AssetCreate, AssetResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Intelligence Platform",
    version="0.1.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/assets", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        owner=asset.owner,
        criticality=asset.criticality
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.get("/assets", response_model=list[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return assets
