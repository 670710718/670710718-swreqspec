# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Booking
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot, db):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["slot_id"] == slot.id
    assert payload["queue_no"]

    db.refresh(slot)
    assert slot.remaining == 0
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1


def test_TC_BKG_01_1_booking_success(client, make_slot, db):
    """TC-BKG-01-1: มีที่นั่งว่าง 1 ที่ เมื่อยืนยันการจองแล้ว ระบบต้องบันทึกสำเร็จ แสดงหมายเลขคิว และเหลือ 0 ที่"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกการจองสำเร็จ; แสดงหมายเลขคิว; ที่นั่งว่างของช่วงนั้นกลายเป็น 0
    assert res.status_code == 201
    payload = res.json()
    assert payload["queue_no"]
    assert payload["slot_id"] == slot.id

    db.refresh(slot)
    assert slot.remaining == 0
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1


def test_TC_BKG_01_2_last_seat_booking(client, make_slot, db):
    """TC-BKG-01-2: ที่นั่งสุดท้าย 1 ที่ เมื่อยืนยันการจอง ระบบต้องบันทึกสำเร็จ และลดเหลือ 0"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่างเพียง 1 ที่ (เป็นที่นั่งสุดท้ายก่อนยืนยัน)
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกการจองสำเร็จ; แสดงหมายเลขคิว; ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0
    assert res.status_code == 201
    payload = res.json()
    assert payload["queue_no"]
    assert payload["slot_id"] == slot.id

    db.refresh(slot)
    assert slot.remaining == 0
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1


def test_TC_BKG_01_3_unverified_user(client, make_slot):
    """TC-BKG-01-3: ยังไม่ยืนยันตัวตน จนกว่าความต้องการถูกกำหนดชัดจะยังไม่ตรวจได้ (รอ Q-03)"""
    # Given: ยังไม่ยืนยันตัวตน แต่ช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: พยายามยืนยันการจองช่วง 09.00 น.
    client.post("/bookings", json={"slot_id": slot.id}, headers={"Authorization": "Bearer invalid"})

    # Then: spec ไม่ได้บอกว่าระบบควรปฏิเสธอย่างไรหรือแสดงข้อความใด (รอ Q-03)
    # ยังไม่ตรวจเพราะรอ Q-03
    return
