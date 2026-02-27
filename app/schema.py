# hostname = 'localhost'
# database = 'portgresql-db'
# username = 'root'
# password = 'root'
# port_id  = 5432

import sqlalchemy

pg_engine = sqlalchemy.create_engine(
    "postgresql+psycopg2://root:root@portgres:5432/crypto", echo=True
)
mariadb_engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:root@mariadb:3306/mariadb_db", echo=True
)

pg_connection = pg_engine.connect()
mariadb_connection = mariadb_engine.connect()

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "crypto",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("price", sqlalchemy.Numeric(18, 8)),
    sqlalchemy.Column("quantity", sqlalchemy.Numeric(18, 8)),
)
metadata.create_all(mariadb_engine)
metadata.create_all(pg_engine)


def mariadb_insert_data(price: float, quantity: float) -> None:
    query = user_table.insert().values(price=price, quantity=quantity)
    with mariadb_engine.connect() as conn:
        conn.execute(query)
        conn.commit()
