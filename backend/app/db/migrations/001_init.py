"""Initial migration: create slots, bookings, audit_logs tables.
"""
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Time, DateTime, ForeignKey


def upgrade(engine):
    meta = MetaData()
    meta.bind = engine

    Table(
        "slots",
        meta,
        Column("id", Integer, primary_key=True),
        Column("slot_date", Date, nullable=False),
        Column("start_time", Time, nullable=False),
        Column("package_code", String, nullable=False),
        Column("capacity", Integer, nullable=False),
        Column("remaining", Integer, nullable=False),
    ).create(engine, checkfirst=True)

    Table(
        "bookings",
        meta,
        Column("id", Integer, primary_key=True),
        Column("hn", String, nullable=False, index=True),
        Column("slot_id", Integer, ForeignKey("slots.id"), nullable=False),
        Column("booking_date", DateTime, nullable=False),
        Column("queue_no", String, nullable=True),
        Column("status", String, nullable=False),
        Column("created_at", DateTime, nullable=False),
    ).create(engine, checkfirst=True)

    Table(
        "audit_logs",
        meta,
        Column("id", Integer, primary_key=True),
        Column("actor_id", String, nullable=False),
        Column("action", String, nullable=False),
        Column("hn", String, nullable=True),
        Column("accessed_at", DateTime, nullable=False),
    ).create(engine, checkfirst=True)


def downgrade(engine):
    meta = MetaData()
    meta.bind = engine
    for t in ("audit_logs", "bookings", "slots"):
        Table(t, meta).drop(engine, checkfirst=True)
