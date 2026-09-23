import sqlalchemy as sa
from sqlalchemy import create_engine, inspect
from app.db.migrations import 001_init as migration_module


def test_migration_creates_tables_and_columns():
    # ใช้ SQLite in-memory เพื่อทดสอบ migration (ตาม plan: pytest ใช้ sqlite:///:memory:)
    engine = create_engine("sqlite:///:memory:")

    # Run upgrade
    migration_module.upgrade(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "slots" in tables
    assert "bookings" in tables
    assert "audit_logs" in tables

    # ตรวจ columns ของ bookings
    cols = {c[1] for c in inspector.get_columns("bookings")}
    # ต้องมี hn, slot_id, booking_date, queue_no, status, created_at
    for expected in ("hn", "slot_id", "booking_date", "queue_no", "status", "created_at"):
        assert expected in cols

    # ต้องไม่มีคอลัมน์ national_id ตาม IF-HIS-01
    assert "national_id" not in cols
