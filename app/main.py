from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import engine, SessionLocal
from app.db.models import Base, Asset
from app.db.schemas import AssetCreate, AssetResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Intelligence Platform",
    version="0.2.0"
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


@app.get("/assets/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@app.get("/assets/critical/list", response_model=list[AssetResponse])
def get_critical_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.criticality == "high").all()
    return assets


@app.put("/assets/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, updated_asset: AssetCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    asset.name = updated_asset.name
    asset.asset_type = updated_asset.asset_type
    asset.owner = updated_asset.owner
    asset.criticality = updated_asset.criticality

    db.commit()
    db.refresh(asset)

    return asset


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()

    return {"message": f"Asset {asset_id} deleted successfully"}
