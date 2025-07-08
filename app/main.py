from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
import pandas as pd

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def list_clans(db: Session = Depends(get_db)):
    """Return all clans in the database."""
    return crud.get_all_clans(db)

# Upload CSV to create clans
@app.post("/upload_csv")
def upload_csv(db: Session = Depends(get_db)):
    """Import clans from ``sample_data.csv`` and store them."""
    df = pd.read_csv("sample_data.csv")
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
    df.to_csv("exported_clans.csv", index=False)    return {"message": "Clans exported to CSV successfully."}
