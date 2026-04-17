from pydantic import BaseModel


class AssetCreate(BaseModel):
    name: str
    asset_type: str
    owner: str
    criticality: str


class AssetResponse(BaseModel):
    id: int
    name: str
    asset_type: str
    owner: str
    criticality: str

    class Config:
        from_attributes = True


class RelationCreate(BaseModel):
    source_asset_id: int
    target_asset_id: int
    relation_type: str


class RelationResponse(BaseModel):
    id: int
    source_asset_id: int
    target_asset_id: int
    relation_type: str

    class Config:
        from_attributes = True
