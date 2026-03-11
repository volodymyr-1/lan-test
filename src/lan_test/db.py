"""db.py - SQLite async storage for request history."""
import aiosqlite
import os
from datetime import datetime
from .models import RequestRecord

DB_PATH = os.getenv("DB_PATH", "lan_test.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                question    TEXT NOT NULL,
                provider    TEXT NOT NULL,
                quality     REAL NOT NULL,
                saved       INTEGER NOT NULL,
                latency_ms  REAL NOT NULL,
                created_at  TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_request(rec: RequestRecord) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO requests (question, provider, quality, saved, latency_ms, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (rec.question, rec.provider, rec.quality,
             int(rec.saved), rec.latency_ms,
             rec.created_at.isoformat()),
        )
        await db.commit()
        return cursor.lastrowid


async def get_history(limit: int = 50) -> list[RequestRecord]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM requests ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
    return [
        RequestRecord(
            id=r["id"], question=r["question"], provider=r["provider"],
            quality=r["quality"], saved=bool(r["saved"]),
            latency_ms=r["latency_ms"],
            created_at=datetime.fromisoformat(r["created_at"]),
        )
        for r in rows
    ]


async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        total  = (await (await db.execute("SELECT COUNT(*) FROM requests")).fetchone())[0]
        saved  = (await (await db.execute("SELECT COUNT(*) FROM requests WHERE saved=1")).fetchone())[0]
        avg_q  = (await (await db.execute("SELECT AVG(quality) FROM requests")).fetchone())[0]
        by_provider = await (await db.execute(
            "SELECT provider, COUNT(*) as cnt FROM requests GROUP BY provider ORDER BY cnt DESC"
        )).fetchall()
    return {
        "total":       total,
        "saved":       saved,
        "avg_quality": round(avg_q or 0, 2),
        "by_provider": {row[0]: row[1] for row in by_provider},
    }
