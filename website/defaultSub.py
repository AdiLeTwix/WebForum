from .models import Subject
from . import db

def GetSupp():
    try_sub = Subject.query.filter_by(name="Supprimé").first()
    if not try_sub:
        supp = Subject(name="Supprimé")
        db.session.add(supp)
        db.session.commit
        return GetSupp()
    return try_sub