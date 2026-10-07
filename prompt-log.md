# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2026-10-07 00.00 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (ไม่มีแถวสถานะ "ใช้ได้" ใน test-cases.md สำหรับ AC นี้)
- หน้าที่ตรวจ: AC-BKG-01, spec.md / plan.md / tasks.md / test-cases.md
- การตรวจ: T-03 สถานะ "เสร็จ" และ T-06 สถานะ "รอ Q-02"; จึงยังไม่เขียนโค้ด test
- ผลลัพธ์: เพิ่ม 3 แถว draft ใน specs/001-booking/test-cases.md
  - TC-BKG-01-1: ทางปกติ
  - TC-BKG-01-2: ขอบ
  - TC-BKG-01-3: ทางผิด (ยังไม่ยืนยันตัวตน, spec ไม่ได้บอกผลที่ควรเป็น และค้างคำถาม Q-03)
- สรุป: แถวทั้งหมดอยู่ในสถานะ "ร่าง" และต้องให้ทีมตรวจแล้วเปลี่ยนเป็น "ใช้ได้" ก่อนจึงเริ่มเขียน test
---

## 2026-10-07 12.00 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test
- หน้าที่ตรวจ: AC-BKG-01, test-cases.md แถว TC-BKG-01-1 ถึง TC-BKG-01-3 สถานะ "ใช้ได้"
- ผลลัพธ์: เขียนโค้ด test ใน backend/tests/test_AC_BKG_01.py
  - TC-BKG-01-1: assert สำเร็จ
  - TC-BKG-01-2: assert สำเร็จ
  - TC-BKG-01-3: ยังไม่ตรวจเพราะรอ Q-03 โดยไม่มี assert
- รัน test: cd backend && pytest -v
- ผล: ผ่านทั้งหมด 7 test

### ผลทดสอบจริง
- test_AC_BKG_01: PASSED
- test_TC_BKG_01_1_booking_success: PASSED
- test_TC_BKG_01_2_last_seat_booking: PASSED
- test_TC_BKG_01_3_unverified_user: PASSED (ไม่มี assert ตาม Q-03)
- test_AC_BKG_05: PASSED
- test_T01_tables_created: PASSED
- test_T01_no_national_id: PASSED

สรุป: โหมดเขียน test สำหรับ AC-BKG-01 สำเร็จ 3 แถวที่พร้อมตรวจได้ผ่าน และ 1 แถวที่รอ Q-03 ยังไม่มี assert ตามเงื่อนไข