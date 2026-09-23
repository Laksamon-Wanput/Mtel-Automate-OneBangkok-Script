# OneBangkok Script

สคริปต์นี้ใช้ค้นหา Notification ของ account จากอีเมล โดยทำงานตามลำดับดังนี้:

1. ค้นหา `account_id` จากฐาน `ob_iam_uat`
2. ค้นหา `recipient_id` จากฐาน `ob_notification_uat`
3. ค้นหา message ที่มีข้อความตามค่า `NOTIFICATION_MESSAGE` ใน `.env`

## การติดตั้ง

ต้องมี Python 3 และเชื่อมต่อ network/VPN ที่เข้าถึงฐาน UAT ได้ จากนั้นติดตั้ง package:

```bash
python3 -m pip install 'psycopg[binary]>=3.2,<4'
```

## การตั้งค่า

วางไฟล์ `.env` ที่ root ของโปรเจกต์ โดยต้องมีตัวแปรต่อไปนี้:

```env
IAM_DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/ob_iam_uat"
Notification_DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/ob_notification_uat"
NOTIFICATION_MESSAGE="Check your coupon details for eligible items"
```

> ห้าม commit หรือ push ไฟล์ `.env` ที่มี username/password จริงขึ้น GitHub

## วิธี Run

เข้าไปที่ root ของโปรเจกต์:

```bash
cd "/Users/wanputlaksamon/Projects/OneBangkok-Script"
```

รันโดยระบุอีเมลที่ต้องการค้นหา:

```bash
python3 'Shuttlebus/Find notification from email&message' --email 'wanput.lak+4@mtel.co.th'
```

แสดง `message.data` ของแต่ละ row ที่พบ:

```bash
python3 'Shuttlebus/Find notification from email&message' \
  --email 'wanput.lak+4@mtel.co.th' \
  --show-data
```

ค้นหาข้อความอื่นชั่วคราว โดยไม่ต้องแก้ `.env`:

```bash
python3 'Shuttlebus/Find notification from email&message' \
  --email 'wanput.lak+4@mtel.co.th' \
  --message 'ข้อความที่ต้องการค้นหา'
```

ดูตัวเลือกทั้งหมด:

```bash
python3 'Shuttlebus/Find notification from email&message' --help
```

## ผลลัพธ์

เมื่อพบข้อมูล สคริปต์จะแสดง `account_id`, `recipient_id`, message ID และจำนวน row:

```text
FOUND: พบข้อมูลทั้งหมด 2 row(s)
```

เมื่อไม่พบข้อมูล สคริปต์จะแสดง error และคืน exit code `1`:

```text
ERROR: ไม่พบ message ที่มีข้อความ "..." สำหรับ email ...
```

หาก Terminal ค้างที่ `dquote>` ให้กด `Ctrl+C` แล้วรันคำสั่งใหม่ โดยตรวจว่าเครื่องหมาย quote `'` หรือ `"` ปิดครบคู่
