from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
)

Base = declarative_base()


class Slot(Base):
    """รองรับ: FR-BKG-01, FR-BKG-06, CON-TECH-01"""
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    package_code = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    remaining = Column(Integer, nullable=False)
    bookings = relationship("Booking", back_populates="slot")


class Booking(Base):
    """รองรับ: FR-BKG-02, FR-BKG-04, IF-HIS-01, CON-TECH-01"""
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    hn = Column(String, nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    # queue_no รูปแบบยังไม่ได้กำหนด (Q-02)
    queue_no = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    slot = relationship("Slot", back_populates="bookings")


class AuditLog(Base):
    """รองรับ: DOM-PDPA-01"""
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    hn = Column(String, nullable=True)
    accessed_at = Column(DateTime, nullable=False)
