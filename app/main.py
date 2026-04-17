from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import engine, SessionLocal
from app.db import models, schemas
from app.db.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Asset Intelligence Platform",
    version="0.5.0"
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


# -------------------------
# ASSETS
# -------------------------

@app.post("/assets", response_model=schemas.AssetResponse)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = models.Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        owner=asset.owner,
        criticality=asset.criticality
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.get("/assets", response_model=list[schemas.AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()


@app.get("/assets/critical/list", response_model=list[schemas.AssetResponse])
def get_critical_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).filter(models.Asset.criticality == "high").all()


@app.get("/assets/{asset_id}", response_model=schemas.AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@app.put("/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(asset_id: int, updated_asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

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
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()

    return {"message": f"Asset {asset_id} deleted successfully"}


# -------------------------
# RELATIONS
# -------------------------

@app.post("/relations", response_model=schemas.RelationResponse)
def create_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db)):
    source_asset = db.query(models.Asset).filter(
        models.Asset.id == relation.source_asset_id
    ).first()

    target_asset = db.query(models.Asset).filter(
        models.Asset.id == relation.target_asset_id
    ).first()

    if source_asset is None:
        raise HTTPException(status_code=404, detail="Source asset not found")

    if target_asset is None:
        raise HTTPException(status_code=404, detail="Target asset not found")

    existing = db.query(models.AssetRelation).filter(
        models.AssetRelation.source_asset_id == relation.source_asset_id,
        models.AssetRelation.target_asset_id == relation.target_asset_id,
        models.AssetRelation.relation_type == relation.relation_type
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relation already exists")

    db_relation = models.AssetRelation(
        source_asset_id=relation.source_asset_id,
        target_asset_id=relation.target_asset_id,
        relation_type=relation.relation_type
    )

    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)

    return db_relation


@app.get("/relations", response_model=list[schemas.RelationResponse])
def get_relations(db: Session = Depends(get_db)):
    return db.query(models.AssetRelation).all()


@app.get("/assets/{asset_id}/dependencies")
def get_asset_dependencies(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    relations = db.query(models.AssetRelation).filter(
        models.AssetRelation.source_asset_id == asset_id
    ).all()

    result = []
    for relation in relations:
        target_asset = db.query(models.Asset).filter(
            models.Asset.id == relation.target_asset_id
        ).first()

        if target_asset:
            result.append({
                "relation_id": relation.id,
                "relation_type": relation.relation_type,
                "target_asset": {
                    "id": target_asset.id,
                    "name": target_asset.name,
                    "asset_type": target_asset.asset_type,
                    "owner": target_asset.owner,
                    "criticality": target_asset.criticality
                }
            })

    return {
        "asset_id": asset.id,
        "asset_name": asset.name,
        "dependencies": result
    }


@app.get("/assets/{asset_id}/impact")
def get_impact(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    visited = set()
    to_visit = [asset_id]
    impacted = []

    while to_visit:
        current = to_visit.pop()

        relations = db.query(models.AssetRelation).filter(
            models.AssetRelation.source_asset_id == current
        ).all()

        for relation in relations:
            target_id = relation.target_asset_id

            if target_id not in visited:
                visited.add(target_id)

                target_asset = db.query(models.Asset).filter(
                    models.Asset.id == target_id
                ).first()

                if target_asset:
                    impacted.append({
                        "id": target_asset.id,
                        "name": target_asset.name,
                        "type": target_asset.asset_type,
                        "criticality": target_asset.criticality
                    })

                to_visit.append(target_id)

    return {
        "asset_id": asset_id,
        "impacted_assets": impacted
    }


@app.get("/assets/{asset_id}/risk")
def calculate_risk(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    criticality_score = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    base = criticality_score.get(asset.criticality, 1)

    relations = db.query(models.AssetRelation).filter(
        models.AssetRelation.source_asset_id == asset_id
    ).all()

    dependency_count = len(relations)
    risk_score = base + dependency_count

    return {
        "asset_id": asset.id,
        "asset_name": asset.name,
        "criticality": asset.criticality,
        "dependencies": dependency_count,
        "risk_score": risk_score
    }
