from sqlalchemy.orm import Session
from . import models, schemas

def create_clan(db: Session, clan: schemas.ClanCreate):
    """Insert a new ``Clan`` record into the database."""
    db_clan = models.Clan(name=clan.name, region=clan.region)
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

def get_all_clans(db: Session):
    """Return all ``Clan`` records from the database."""
    return db.query(models.Clan).all()
