# แผนงานฟีเจอร์: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง
ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้ว เลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ แล้วได้รับหมายเลขคิว โดยใช้กระบวนการตรวจสอบความซ้ำของคิวในวันเดียวกันและจัดการกรณีช่วงเวลาที่เลือกเต็มด้วยข้อเสนอ 3 ตัวเลือกในวันเดียวกันหรือวันถัดไป ระบบจะบันทึกการจองก่อน แล้วส่งคำขอ SMS/LINE แบบ asynchronous เพื่อไม่ให้การจองถูกหยุดรอข้อความยืนยัน และจะบันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจองตามข้อกำหนดด้านความปลอดภัย

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจอง ช่วงเวลา audit log และข้อความแจ้งเตือน |
| Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | จัดการ REST API สำหรับการค้นหาช่วงเวลา การตรวจคิวซ้ำ และการยืนยันการจอง |
| React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | จัดการหน้าเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ |
| ระบบแจ้งเตือน SMS/LINE แบบ asynchronous | IF-NOT-01 | ส่งข้อความยืนยันผ่าน queue/background worker เพื่อไม่ทำให้การจองรอผลส่งข้อความ |
| ระบบยืนยันตัวตนภายนอก | IF-IDP-01 | ใช้เป็น precondition ก่อนเข้าถึงข้อมูลผู้รับบริการ |
| HIS integration ด้วย HN | IF-HIS-01 | ค้นข้อมูลผู้รับบริการจาก HIS แล้วแปลงเป็น HN ภายในระบบ ไม่บันทึกเลขบัตรประชาชน |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ FR/Constraint |
|---|---|---|
| Booking | booking_id, patient_hn, package_id, booking_date, slot_id, status, queue_no, created_at, confirmed_at | FR-BKG-02, FR-BKG-04, FR-BKG-05, DOM-PDPA-01 |
| BookingSlot | slot_id, date, start_time, end_time, quota_total, quota_remaining | FR-BKG-01, FR-BKG-03, FR-BKG-06 |
| QueueTicket | queue_id, booking_id, queue_no, issue_date | FR-BKG-04, Q-02 (ยังไม่ชัด) |
| AuditLog | audit_id, accessor_user, accessed_hn, accessed_at, action_type | DOM-PDPA-01 |
| NotificationRequest | notification_id, booking_id, channel, payload, status, enqueue_at, retry_count | FR-BKG-05, IF-NOT-01, NFR-REL-02 |
| PatientProfile | hn, identity_verified_at, last_updated_at | IF-IDP-01, IF-HIS-01 |

หมายเหตุเพิ่มเติม:
- ไม่เก็บเลขบัตรประชาชนในตาราง Booking ตาม IF-HIS-01
- BookingSlot จะเก็บจำนวนที่นั่งคงเหลือสำหรับแต่ละช่วงเวลาเพื่อรองรับ FR-BKG-01 และ FR-BKG-03
- QueueTicket ใช้เพื่อแสดงหมายเลขคิวเดิมเมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกันตาม FR-BKG-02

## 4. API / หน้าจอ

| รายการ | Method / Path | Input / Output หลัก | รองรับ |
|---|---|---|---|
| หน้ารายการวันและช่วงเวลา | GET /booking/slots | dateFrom, dateTo, packageId -> รายการวัน/ช่วงเวลา + ที่นั่งคงเหลือ | FR-BKG-01, FR-BKG-06 |
| ตรวจคิวซ้ำ | POST /booking/validate-duplicate | hn, bookingDate -> status: allowed/blocked, queueNo เดิม | FR-BKG-02 |
| เสนอช่วงเวลาอื่น | POST /booking/alternative-slots | packageId, selectedSlot, date -> 3 ตัวเลือกที่ใกล้ที่สุด | FR-BKG-03 |
| ยืนยันการจอง | POST /booking/confirm | hn, packageId, date, slotId, userId -> booking_id, queue_no, status | FR-BKG-04 |
| ส่งข้อความยืนยันแบบ async | POST /booking/notifications | booking_id, channel, payload -> queued job id | FR-BKG-05, IF-NOT-01 |
| ดูประวัติการเข้าถึงข้อมูล | GET /booking/audit-log | hn หรือ booking_id -> รายการ audit log | DOM-PDPA-01 |

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | MySQL ถูกใช้เป็นฐานข้อมูลหลักสำหรับ Booking, BookingSlot, AuditLog, NotificationRequest | ใช้แล้ว |
| DOM-PDPA-01 | AuditLog model และ endpoint ดูประวัติการเข้าถึงข้อมูล | ใช้แล้ว |
| IF-IDP-01 | precondition สำหรับการอนุญาตเข้าใช้งานฟีเจอร์ และควรเรียกก่อนเปิดข้อมูลผู้รับบริการ | ใช้แล้ว |
| IF-HIS-01 | PatientProfile และการจัดเก็บ HN แทนเลขบัตรประชาชนใน Booking | ใช้แล้ว |
| IF-NOT-01 | NotificationRequest และ background worker สำหรับ SMS/LINE เป็น asynchronous | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_booking_confirm_success | ตั้งค่าช่วง 09.00 มีที่นั่ง 1 ที่ ยืนยันการจอง แล้วตรวจว่า booking ถูกบันทึก queue_no แสดงบนหน้าจอ และ quota_remaining เป็น 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_duplicate_queue_same_day | ตั้งค่าสถานะ “มีคิวที่ยังไม่ได้ใช้” ในวันเดียวกัน แล้วลองจองใหม่ ต้องปฏิเสธและแสดง queue_no เดิม |
| AC-BKG-03 | test_AC_BKG_03_offer_alternatives_when_slot_full | ตั้งช่วงที่เลือกเต็มและอีกผู้ใช้ยืนยันก่อนแล้ว ตรวจว่าเว็บไซต์แจ้ง “ช่วงเวลาเต็ม” และเสนอ 3 ตัวเลือกในวันเดียวกันหรือวันถัดไปที่ยังมีที่นั่งว่าง |
| AC-BKG-04 | test_AC_BKG_04_booking_saved_when_notification_fails | จำลอง SMS/LINE ส่งไม่สำเร็จ ตรวจว่าการจองยังถูกบันทึก ปรากฏ queue_no และมี record ใน retry queue ภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_slot_search_p95_under_2s | จำลองผู้ใช้พร้อมกัน 200 คน ค้นหาช่วงเวลาว่าง แล้วตรวจ p95 ของ response time <= 2 วินาที |
| AC-BKG-06 | test_AC_BKG_06_audit_log_recorded | เปิดดูข้อมูลการจองของผู้รับบริการ แล้วตรวจว่า audit log มีผู้เข้าถึง เวลา และ HN/รหัสผู้รับบริการ |

## 7. ลำดับงาน

1. สร้าง schema ฐานข้อมูลพื้นฐาน: Booking, BookingSlot, AuditLog, NotificationRequest และข้อมูลผู้รับบริการแบบจำกัดตาม HN (FR-BKG-01, FR-BKG-04, DOM-PDPA-01)
2. สร้าง API ค้นหาช่วงเวลาว่างและจำนวนที่นั่งคงเหลือ พร้อมกรองตามแพ็กเกจและ 30 วันข้างหน้า (FR-BKG-01, FR-BKG-06, AC-BKG-05)
3. สร้าง workflow ตรวจคิวซ้ำในวันเดียวกันและแสดงหมายเลขคิวเดิม (FR-BKG-02, AC-BKG-02)
4. สร้าง logic เมื่อช่วงเวลาที่เลือกเต็ม ให้แจ้งเตือนและเสนอ 3 ตัวเลือกที่ใกล้ที่สุดในวันเดียวกันหรือวันถัดไป (FR-BKG-03, AC-BKG-03)
5. สร้าง workflow ยืนยันการจอง: บันทึก booking, ตัดจำนวนที่นั่ง, ออกหมายเลขคิว, ส่งคำขอแจ้งเตือนแบบ async (FR-BKG-04, AC-BKG-01)
6. สร้าง queue worker และ retry logic สำหรับ SMS/LINE ที่ส่งไม่สำเร็จ พร้อมรักษาการจองให้ยังอยู่ (FR-BKG-05, NFR-REL-02, AC-BKG-04)
7. เพิ่ม audit log ทุกครั้งที่เข้าถึงข้อมูลการจองในฐานข้อมูลและ API (DOM-PDPA-01, AC-BKG-06)
8. ตรวจความพร้อม UI และ integration testing กับ 200 concurrent users, confirm flow, และ validation ของข้อเสนอช่วงเวลา (AC-BKG-03, AC-BKG-05)

## 8. สิ่งที่ยังไม่ทำ
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง? -> ต้องถามเจ้าหน้าที่เวชระเบียน
  ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ
