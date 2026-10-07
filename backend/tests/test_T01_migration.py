import importlib.util
from pathlib import Path
from sqlalchemy import create_engine, inspect


def load_migration_module():
    # โหลดไฟล์ migration ที่ชื่อเริ่มด้วยตัวเลขโดยใช้ importlib
    path = Path(__file__).resolve().parents[1] / "app" / "db" / "migrations" / "001_init.py"
    spec = importlib.util.spec_from_file_location("migration_001_init", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_migration_creates_tables_and_columns():
    # ใช้ SQLite in-memory เพื่อทดสอบ migration (ตาม plan: pytest ใช้ sqlite:///:memory:)
    engine = create_engine("sqlite:///:memory:")

    migration_module = load_migration_module()

    # Run upgrade
    migration_module.upgrade(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "slots" in tables
    assert "bookings" in tables
    assert "audit_logs" in tables

    # ตรวจ columns ของ bookings
    cols = {c["name"] for c in inspector.get_columns("bookings")}
    # ต้องมี hn, slot_id, booking_date, queue_no, status, created_at
    for expected in ("hn", "slot_id", "booking_date", "queue_no", "status", "created_at"):
        assert expected in cols

    # ต้องไม่มีคอลัมน์ national_id ตาม IF-HIS-01
    assert "national_id" not in cols
