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
