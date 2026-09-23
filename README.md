# OneBangkok Script

This script checks whether an account has received a notification containing a specified message. It follows these steps:

1. Find the `account_id` for an email address in `ob_iam_uat`.
2. Find the `recipient_id` for that account in `ob_notification_uat`.
3. Count matching notifications using `NOTIFICATION_MESSAGE` from `.env`.

## Requirements

Install Python 3 and connect to the network or VPN that can access the UAT databases. Then install the PostgreSQL driver:

```bash
python3 -m pip install 'psycopg[binary]>=3.2,<4'
```

## Configuration

Place a `.env` file in the project root with these values:

```env
IAM_DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/ob_iam_uat"
Notification_DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/ob_notification_uat"
NOTIFICATION_MESSAGE="Check your coupon details for eligible items"
```

Replace the database placeholders with your UAT connection details. Keep `.env` private; it may contain a database password.

## Run the script

Open a terminal in the project root. For this checkout:

```bash
cd "/Users/wanputlaksamon/Projects/OneBangkok-Script"
```

Search for an email address:

```bash
python3 'Shuttlebus/Find notification from email&message' --email 'wanput.lak+4@mtel.co.th'
```

To print the `message.data` value for each matching row, add `--show-data`:

```bash
python3 'Shuttlebus/Find notification from email&message' \
  --email 'wanput.lak+4@mtel.co.th' \
  --show-data
```

To search for a different message without changing `.env`, use `--message`:

```bash
python3 'Shuttlebus/Find notification from email&message' \
  --email 'wanput.lak+4@mtel.co.th' \
  --message 'Another notification message'
```

To see all options:

```bash
python3 'Shuttlebus/Find notification from email&message' --help
```

## Results

The script logs the account and recipient lookup results, then prints the number of matching message rows. A successful result looks like this:

```text
FOUND: พบข้อมูลทั้งหมด 2 row(s)
```

The script currently prints some status and error messages in Thai. If no matching message is found, it prints an `ERROR` and exits with code `1`.

If your terminal shows `dquote>`, press `Ctrl+C` and rerun the command. This prompt means a double quote (`"`) was left open.
