import pony.orm.dbproviders.sqlite


from pony.orm import (
    Required,
    PrimaryKey,
    Set,
    Optional,
    Database,
    db_session,
    min,
    TransactionIntegrityError,
)
from pony.orm.ormtypes import IntArray
import datetime
from mydevoirs.constants import MATIERES
from mydevoirs.utils import get_dir

from .base_db import db, GetOrCreateMixin


class Jour(db.Entity, GetOrCreateMixin):
    date = PrimaryKey(datetime.date)
    items = Set("Item")

    @classmethod
    def oldest(cls):
        return min(i.date for i in cls)


class Matiere(db.Entity):
    # id = PrimaryKey(int, auto=True)
    nom = PrimaryKey(str)
    color = Required(IntArray)
    items = Set("Item")


class Item(db.Entity):
    id = PrimaryKey(int, auto=True)
    matiere = Required(Matiere, default="Français")
    jour = Required(Jour)
    content = Optional(str)
    done = Required(bool, default=False)

    def toggle(self):
        self.done = not self.done


@db.on_connect(provider="sqlite")
def sqlite_synchonous_off(db, connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA synchronous = OFF")


###################################################################
############## DATABASE SETUP #####################################
###################################################################

light_db = get_dir("cache") / "ddb.sqlite"
hard_db = get_dir("cache") / "ddb_hard.sqlite"
# db.bind(provider="sqlite", filename=":memory:")
# db.bind(provider="sqlite", filename=str(light_db.absolute()), create_db=True)
db.bind(provider="sqlite", filename=str(hard_db.absolute()), create_db=True)
# if not light_db.is_file():
db.generate_mapping(create_tables=True)

with db_session():
    for k, v in MATIERES.items():
        try:
            Matiere(nom=k, color=v)
            db.commit()
        except TransactionIntegrityError:
            pass

# with db_session():

#     a= Jour.get(date=datetime.date(2019,11,1)) or Jour(date=datetime.date(2019,11,1))

#     m = Matiere[MATIERES[0]]
#     n = Matiere[MATIERES[2]]
#     Item(matiere=m, jour=a, content="blablabal lablab")
#     Item(matiere=m, jour=a, content="bLe deuxième")