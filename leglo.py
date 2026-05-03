from pony import orm

DB = orm.Database()
class Leglo(DB.Entity):
    id = orm.PrimaryKey(int, auto = True)
    roditelj1 = orm.Required(orm.Json)
    roditelj2 = orm.Required(orm.Json)

    rezultat = orm.Optional(orm.Json)

DB.bind(provider="sqlite", filename="kreirano_leglo.sqlite", create_db = True)
DB.generate_mapping(create_tables=True)