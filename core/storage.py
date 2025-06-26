from csv import writer
from sqlite3 import connect
from pathlib import Path
from typing import Iterable
from core.models import CoinRecord

DDL = """
CREATE TABLE IF NOT EXISTS coins(
    rank        INTEGER PRIMARY KEY,
    name        TEXT,
    symbol      TEXT,
    price_usd   REAL,
    change_24h  REAL,
    market_cap  REAL
);
DELETE FROM coins;
INSERT INTO coins VALUES (?,?,?,?,?,?);
"""

def dump_to_csv(out: Path, records: Iterable[CoinRecord]) -> None:
    """
    Save coin records into a CSV file.

    Args:
        out: Path to the output CSV file.
        records: Iterable of `CoinRecord` instances to write.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        csv_writer = writer(f)
        csv_writer.writerow(
            ["rank", "name", "symbol", "price_usd", "change_24h", "market_cap"]
        )
        for rec in records:
            csv_writer.writerow(rec.as_row())


def dump_to_sqlite(db: Path, records: Iterable[CoinRecord]) -> None:
    """
    Save coin records into a SQLite database.

    Args:
        db: Path to the SQLite file to create or overwrite.
        records: Iterable of `CoinRecord` instances to insert.
    """
    db.parent.mkdir(parents=True, exist_ok=True)
    with connect(db) as conn:
        cur = conn.cursor()
        cur.executescript(DDL.split("DELETE")[0])
        cur.execute("DELETE FROM coins")
        rows = [rec.as_row() for rec in records]
        cur.executemany("INSERT INTO coins VALUES (?,?,?,?,?,?)", rows)
        conn.commit()
