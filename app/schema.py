# hostname = 'localhost'
# database = 'portgresql-db'
# username = 'root'
# password = 'root'
# port_id  = 5432

import sqlalchemy

pg_engine = sqlalchemy.create_engine(
    "postgresql+psycopg2://root:root@localhost:5432/crypto", echo=True
)
mysql_engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:root@localhost:3306/myapp", echo=True
)

pg_connection = pg_engine.connet()
mysql_connection = mysql_engine.connect()

metadata = sqlalchemy.Metadata()

user_table = sqlalchemy.Table(
    "user",
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Coulmn("price", sqlalchemy.Float),
    sqlalchemy.Column("quantity", sqlalchemy.Float),
)


def sql_insert_data(price: float, quantity: float) -> None:
    query = user_table.insert().values(price=price, quantity=quantity)
    mysql_connection.excute(query)
