# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-07 08:40 | test: 7 ผ่าน, 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/router.py:get_slots; backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py: PASSED | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ยังไม่มีโค้ดที่ปฏิเสธจองซ้ำวันเดียวกัน | ไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ยังไม่มี implementation ที่เสนอ 3 ตัวเลือกเมื่อเต็ม | ไม่มี | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py:create_booking; backend/app/booking/service.py:create_booking, next_queue_no | backend/tests/test_AC_BKG_01.py: PASSED | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 | ยังไม่มีคิวส่งข้อความซ้ำ และยังไม่มีการบันทึกค้างส่ง | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 | backend/app/slots/router.py:get_slots; backend/app/slots/service.py:list_available_slots | ไม่ได้มี test รายละเอียดแพ็กเกจย้าย | ครบ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py: PASSED | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี | ไม่มี | ไม่มี | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ยังไม่มีคิวส่งซ้ำภายใน 5 นาที | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี | ไม่มี | ไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py; backend/app/db/session.py; backend/app/db/models.py | backend/tests/test_T01_schema.py: PASSED | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | backend/app/db/models.py:AuditLog; ยังไม่มี middleware ที่บันทึกทุกการเข้าถึง | backend/tests/test_T01_schema.py: PASSED (schema) แต่ไม่มี test audit log | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py:get_verified_hn | backend/tests/test_AC_BKG_01.py: ผ่าน | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | backend/app/db/models.py:Booking ไม่มี national_id; ยังไม่มี lookup HIS | backend/tests/test_T01_schema.py: PASSED | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ยังไม่มีคิว asynchronous และยังไม่มีการส่งซ้ำ | ไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/service.py:list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ขอบเขตเป็น 14 วัน ไม่ใช่ 30 วัน ตาม FR-BKG-01; รายการแสดงเฉพาะ remaining > 0 แล้วแต่ไม่ทดสอบ 30 วัน |
| backend/app/booking/service.py:create_booking | FR-BKG-04 | ไม่ครบ | ใช้ `slot.remaining < 0` เป็นการตรวจจองเต็มผิด; ถ้า remaining == 0 ยังสามารถลดต่อได้ แม้ task T-05 ยังไม่มีส่วนเสนอ 3 ช่วง |
| backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | ไม่ครบ | กำหนดรูปแบบ `A001` โดยเดาเองจาก Open Question Q-02 ซึ่ง spec ระบุว่า “ยังไม่ได้คำตอบ” |
| backend/app/booking/router.py:create_booking | IF-IDP-01 | ตรง | ใช้ `Depends(get_verified_hn)` ตรวจ token ก่อนรับ booking |
| backend/app/db/models.py:Booking | IF-HIS-01 | ครึ่งหนึ่ง | ไม่มีคอลัมน์ national_id แต่ request model ยังมี `national_id` และ logger ใส่ `national_id` ลง log โดยไม่ได้เก็บในตาราง |
| backend/app/config.py | CON-TECH-01 | ครบ | สร้าง DATABASE_URL ให้ชี้ PostgreSQL ในระบบจริงตาม spec |
| backend/app/main.py:lifespan | CON-TECH-01 | ครบ | สร้างตารางจาก Base metadata; เหมาะกับการทดสอบ SQLite ในหน่วยความจำ |
| frontend/__tests__/AC-BKG-03.test.jsx | FR-BKG-03 | ไม่ครบ | ไม่ผ่านเพราะไม่มีไฟล์ `src/pages/SlotPicker` ที่ test import; ระบุว่า UI ของ “ช่วงเวลาเต็ม + 3 ตัวเลือก” ยังไม่ได้สร้าง |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py:DAYS_AHEAD = 14 | FR-BKG-01 | Spec ระบุแสดงช่วงเวลาภายใน 30 วันข้างหน้า แต่โค้ดกำหนด 14 วันเท่านั้น | แก้โค้ด |
| F-002 | เดา Q-xx | backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | โค้ดใช้รูปแบบ `A001` และรีเซ็ตทุกวัน แม้ Q-02 ระบุว่า “ยังไม่ได้คำตอบ” และ plan ระบุว่า “รอ Q-02” | เพิ่ม Q-xx |
| F-003 | ละเมิด Constraint | backend/app/booking/router.py:BookingRequest.national_id + logger.info | IF-HIS-01 | API รับ field `national_id` และ log ถึง `national_id` แม้ spec บอกว่าไม่เก็บเลขบัตรประชาชนในตารางการจองและต้องอ้าง HN อย่างเดียว | แก้โค้ด |
| F-004 | test อ่อน | backend/tests/test_AC_BKG_01.py | AC-BKG-01, FR-BKG-04 | Test ตรวจเพียง status 201 และมี queue_no ไม่ได้ตรวจว่าหมายเลขคิวตรงตามรูปแบบหรือวันที่มีค่า 0 หลังจอง อย่างรอบคอบ | แก้ spec / เพิ่ม test |
| F-005 | AC ไม่มี test | frontend/__tests__/AC-BKG-03.test.jsx | FR-BKG-03 | test หน้าจอ import `SlotPicker` แต่ไฟล์ที่ใช้ไม่ได้มีอยู่ กรณี “ช่วงเวลาเต็ม + 3 ตัวเลือก” จึงยังไม่มี UI ที่ทำจริง | แก้โค้ด |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| ไม่มี | ยังไม่มีข้อค้นพบที่ได้รับการแก้จากทีมในรอบนี้ | ยังไม่ได้มีการแก้โค้ดหรือ spec โดยหลังจาก verify นี้ |
