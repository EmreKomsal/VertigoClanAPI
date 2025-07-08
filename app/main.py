from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
import pandas as pd



app = FastAPI()


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    """Provide a database session to request handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new clan
@app.post("/clans", response_model=schemas.ClanResponse)
def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_db)):
    """Create a new clan record."""
    return crud.create_clan(db, clan)

# List all clans
@app.get("/clans", response_model=list[schemas.ClanResponse])
def list_clans(
    region: Optional[str] = Query(None),
    sort: Optional[str] = Query(None, regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """Return all clans in the database. with optional filtering and sorting."""
    query = db.query(models.Clan)

    if region:
        query = query.filter(models.Clan.region == region)

    if sort == "asc":
        query = query.order_by(models.Clan.created_at.asc())
    elif sort == "desc":
        query = query.order_by(models.Clan.created_at.desc())

    return query.all()

# Get clan by ID
@app.get("/clans/{clan_id}", response_model=schemas.ClanResponse)
def get_clan(clan_id: str, db: Session = Depends(get_db)):
    """Retrieve a clan by its ID."""
    clan = db.query(models.Clan).filter(models.Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return clan

# DELETE clan by ID
@app.delete("/clans/{clan_id}")
def delete_clan(clan_id: str, db: Session = Depends(get_db)):
    """Delete a clan by its ID."""
    clan = db.query(models.Clan).filter(models.Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db.delete(clan)
    db.commit()
    return {"message": "Clan deleted successfully."}

#TEST SCRIPTS FOR UPLOADING AND EXPORTING CSV

# Upload CSV to create clans
@app.post("/upload_csv")
def upload_csv(db: Session = Depends(get_db)):
    """Import clans from ``clan_sample_data.csv`` and store them."""
    df = pd.read_csv("clan_sample_data.csv")
    for _, row in df.iterrows():
        clan_data = schemas.ClanCreate(name=row["name"], region=row.get("region"))
        crud.create_clan(db, clan_data)
    return {"message": "CSV uploaded successfully."}

# Export clans to CSV
@app.get("/clans/export_csv")
def export_clans_to_csv(db: Session = Depends(get_db)):
    """Export all clans to ``exported_clans.csv``."""
    clans = crud.get_all_clans(db)
    df = pd.DataFrame([
        {
            "id": str(clan.id),
            "name": clan.name,
            "region": clan.region,
            "created_at": clan.created_at.isoformat(),
        }
        for clan in clans
    ])
    df.to_csv("exported_clans.csv", index=False)    
    return {"message": "Clans exported to CSV successfully."}
