import json
import logging

from confluent_kafka import Consumer, KafkaError
from sqlalchemy import Column, Integer, MetaData, Numeric, Table, create_engine, delete, insert, update

pg_engine = create_engine(
    "postgresql+psycopg2://root:root@postgres:5432/crypto", echo=False
)
metadata = MetaData()
crypto_table = Table(
    "crypto",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("price", Numeric(18, 8)),
    Column("quantity", Numeric(18, 8)),
)
metadata.create_all(pg_engine)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

consumer = Consumer(
    {
        "bootstrap.servers": "kafka:29092",
        "group.id": "crypto-consumer-group",
        "auto.offset.reset": "earliest",  # start from beginning if no offset exists
        "enable.auto.commit": True,
    }
)

TOPIC = "dbserver1.mariadb_db.crypto"
consumer.subscribe([TOPIC])

log.info(f"Subscribed to topic: {TOPIC}")


def handle_event(event: dict) -> None:
    op = event.get("op")
    after = event.get("after")
    before = event.get("before")

    with pg_engine.connect() as conn:
        if op == "c":  # insert
            log.info(f"INSERT → {after}")
            conn.execute(
                insert(crypto_table).values(
                    id=after["id"],
                    price=after["price"],
                    quantity=after["quantity"],
                )
            )
            conn.commit()

        elif op == "u":  # update
            log.info(f"UPDATE → {after}")
            conn.execute(
                update(crypto_table)
                .where(crypto_table.c.id == after["id"])
                .values(price=after["price"], quantity=after["quantity"])
            )
            conn.commit()

        elif op == "d":  # delete
            log.info(f"DELETE → id={before['id']}")
            conn.execute(delete(crypto_table).where(
                crypto_table.c.id == before["id"]))
            conn.commit()

        else:
            log.warning(f"Unknown op type: {op} — skipping")


while True:
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            log.error(f"Kafka error: {msg.error()}")
            break

    try:
        payload = json.loads(msg.value().decode("utf-8"))
        handle_event(payload)
    except Exception as e:
        log.error(f"Failed to process message: {e}")
