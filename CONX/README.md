# CONX passenger boarding finder

สคริปต์นี้ค้นหา `passenger_boardings` ด้วย IAM `account_id` โดยใช้ค่าเดียวกันใน
`passenger_boardings.user_id` แล้วแปลงผลลัพธ์เป็นฟิลด์สำหรับ CONX

## ตั้งค่า

คัดลอก `.env.example` เป็น `.env` และใส่ credential:

```bash
cd "/Users/wanputlaksamon/Projects/OneBangkok-Script/CONX"
cp .env.example .env
```

```env
PB_URL=https://uat-qrverify.opsioc.com/api/
PB_ADMIN_EMAIL=admin@mtel.co.th
PB_ADMIN_PASSWORD=YOUR_PASSWORD
PB_INSECURE_TLS=true
```

`.env` ถูก ignore จาก Git แล้ว `PB_INSECURE_TLS=true` ใช้เฉพาะ UAT ที่มี
self-signed certificate เท่านั้น

## ใช้งาน

แสดงผลเป็นตารางใน terminal (`table` เป็นค่าเริ่มต้น):

```bash
python3 find_passenger_boardings.py --account-id 'ACCOUNT_ID'
```

หรือระบุ format ให้ชัดเจนด้วย `--format table`

ระหว่างทำงานสคริปต์จะแสดง log การเชื่อมต่อ, login, หน้าที่กำลังค้นหา และจำนวน
records ที่พบทาง `stderr` จึงไม่ปนกับ JSON/CSV ที่ส่งออกทาง `stdout`

ถ้ารันจาก CONX และทราบ user ที่ login อยู่ ให้ส่งค่าเพื่อใช้ใน `Modified User`:

```bash
python3 find_passenger_boardings.py \
  --account-id 'ACCOUNT_ID' \
  --modified-user 'CURRENT_CONX_USER'
```

หรือกำหนด `CONX_MODIFIED_USER` ใน environment/`.env` หากไม่ระบุ สคริปต์แบบ
standalone จะใช้ email ของ PocketBase admin ที่ login เป็นค่าเริ่มต้น

Export เป็น JSON หรือ CSV:

```bash
python3 find_passenger_boardings.py \
  --account-id 'ACCOUNT_ID' \
  --format json \
  --output result.json

python3 find_passenger_boardings.py \
  --account-id 'ACCOUNT_ID' \
  --format csv \
  --output result.csv
```

สคริปต์ใช้ Python standard library เท่านั้น ไม่ต้องติดตั้ง package เพิ่ม

## Field mapping

| Output | PocketBase source |
|---|---|
| Boarding Location | `passenger_boardings.boarding_location_id` |
| Boarding Time | `passenger_boardings.boarding_time` |
| Bus Reference | `device_id -> devices.bus_id -> buses.name` |
| Bus shift | `passenger_boardings.bus_shift` |
| Created User | `passenger_boardings.user_id` |
| Created Date | `passenger_boardings.created` |
| Customer | `account_id` ที่ใช้ค้นหา |
| Event Id | `passenger_boardings.id` |
| Last Modified | เว้นว่าง |
| Modified User | `--modified-user` / `CONX_MODIFIED_USER` (fallback เป็น PocketBase admin email) |
| Route Name | `trip_id -> device_trips.route_id -> routes.name` |
| Scan Failure Reason | `passenger_boardings.scan_failure_reason` |
| Scan Status | `passenger_boardings.scan_status` |
| Tenant name | `passenger_boardings.tenant_name` |
