## Feature: จองคิวตรวจสุขภาพ
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md
วันที่: 2569-09-22

สรุป: 12 task, 1 task รอ Open Questions

### T-01 สร้างตาราง slots, bookings, audit_logs และ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings`, `audit_logs` สำเร็จ (รัน migration แล้วไม่มี error)
- สถานะ: พร้อมทำ

### T-02 เตรียม session/engine และ config DATABASE_URL
- รองรับ: CON-TECH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02
- ไฟล์ที่แตะ: backend/app/db/session.py, backend/app/config.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: app สร้าง `engine` กับ DATABASE_URL และเชื่อมต่อฐานข้อมูลใน test ได้
- สถานะ: พร้อมทำ

### T-03 GET /slots: คำนวณช่วงว่างและส่งข้อมูล
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05 (performance test ย่อส่วน) และ test unit สำหรับ output structure
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: GET /slots ตอบโครงข้อมูลตามสัญญา และ test unit พื้นฐานผ่าน
- สถานะ: พร้อมทำ

### T-04 POST /bookings พื้นฐาน: ตัดที่นั่ง บันทึกการจอง และคืน booking id
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01 (test_AC_BKG_01)
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py
- ต้องทำหลัง: T-01, T-02, T-03
- เสร็จเมื่อ: POST /bookings สร้าง booking ใน DB และ remaining ลดลงตามที่คาด
- สถานะ: พร้อมทำ

### T-05 กันจองซ้ำวันเดียวกัน (Business rule: ปฏิเสธและคืนหมายเลขคิวเดิม)
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02 (test_AC_BKG_02)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: เมื่อมี booking เดิมในวันเดียวกัน POST /bookings คืน 409 หรือ response ตามสัญญา และ test ที่ตรวจ behavior ผ่าน
- สถานะ: พร้อมทำ

### T-06 เสนอช่วงเวลาใกล้เคียงเมื่อเต็ม (หาจำนวน 3 ตัวเลือก ภายในวันเดียวกันและวันถัดไป)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03 (test_AC_BKG_03 และ AC-BKG-03.test.jsx สำหรับ UI)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/slots/service.py, frontend/src/pages/ConfirmBooking.jsx
- ต้องทำหลัง: T-03, T-04, T-05
- เสร็จเมื่อ: POST /bookings เมื่อเต็มคืน 409 พร้อม payload 3 ช่วงที่ใกล้ที่สุด และหน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" พร้อม 3 ปุ่มตัวเลือก
- สถานะ: พร้อมทำ

### T-07 คิวส่งข้อความ (notify queue) และนโยบายส่งซ้ำตาม ASM-03
- รองรับ: IF-NOT-01, FR-BKG-05, NFR-REL-02
- ตรวจด้วย: AC-BKG-04 (test_AC_BKG_04)
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: POST /bookings วางงานลงคิวไม่รอผล และระบบคิวจำลองสามารถกำหนดงานส่งซ้ำภายใน 5 นาทีได้ (ใน test)
- สถานะ: พร้อมทำ

### T-08 audit middleware: บันทึกการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06 (test_AC_BKG_06)
- ไฟล์ที่แตะ: backend/app/audit/middleware.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: การเรียกดูการจองทำให้มี `audit_logs` ระเบียนที่มี `actor_id`, `accessed_at`, และ `hn` และ test ตรวจพบ
- สถานะ: พร้อมทำ

### T-09 HIS client: GET /patients/lookup เชื่อม IF-HIS-01 (ใช้ mock ใน test)
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ (พื้นฐานของการหา HN) แต่เป็น dependency สำหรับการจอง
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/booking/service.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: endpoint /patients/lookup เรียก client และใน test สามารถ mock ให้คืน `hn` ได้
- สถานะ: พร้อมทำ

### T-10 หน้าจอ SlotPicker (ใช้ API จำลองในหน้าจอ test)
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-USE-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ (หน้าจอช่วยให้ผู้ใช้ทำงาน) และ Vitest test เบื้องต้น
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js, frontend/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: ไม่มี (ใช้ API จำลองตาม rule ใน plan)
- เสร็จเมื่อ: หน้าจอแสดงช่วงเวลาและเปลี่ยนเมื่อเปลี่ยนแพ็กเกจ (mocked API) และ Vitest test พื้นฐานผ่าน
- สถานะ: พร้อมทำ

### T-11 หน้ายืนยัน (ConfirmBooking) — แสดงผล 409 และ 3 ตัวเลือก เมื่อ API จำลองตอบแบบนั้น
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03.test.jsx (UI test) และ integration เล็กๆ กับ mocked POST /bookings
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" พร้อมปุ่ม 3 ตัวเลือก เมื่อ API ตอบ 409
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริง (integration): เชื่อม frontend กับ backend จริงเมื่อ API พร้อม
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ ใหม่ แต่เป็นงานผสานระบบและต้องรัน manual check
- ไฟล์ที่แตะ: frontend/src/api/client.js, vite.config.js
- ต้องทำหลัง: T-03, T-04, T-06
- เสร็จเมื่อ: หน้าจอเรียก API จริงและ workflow จองทำงาน end-to-end ใน dev environment
- สถานะ: รอ Q-02


---

## ตารางตรวจความครบ

1) AC → task
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-04 |
| AC-BKG-02 | T-05 |
| AC-BKG-03 | T-06, T-11 |
| AC-BKG-04 | T-07 |
| AC-BKG-05 | T-03 |
| AC-BKG-06 | T-08 |

2) Constraint → task
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-02 |
| DOM-PDPA-01 | T-01, T-08 |
| IF-IDP-01 | T-02 (integration with auth/idp.py) |
| IF-HIS-01 | T-01, T-09 |
| IF-NOT-01 | T-07 |

ถ้าช่องว่าง: เพิ่ม task จนไม่ว่าง (ขณะนี้ครบตาม spec)

---

## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และรูปแบบ เช่น A001? -> งานที่รอ: T-12 (สถานะ: รอ Q-02)

---

บันทึก: ไม่เริ่มทำโค้ดใด ๆ จนกว่าทีมจะสั่งแยกต่างหาก
