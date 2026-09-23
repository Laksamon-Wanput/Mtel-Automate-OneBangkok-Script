/*
Step 1: Run this query on database ob_iam_uat.
Change params.email to the account email you want to find.
*/
WITH params AS (
    SELECT 'wanput.lak@mtel.co.th'::text AS email
)
SELECT DISTINCT
    identity_row.account_id::text AS account_id
FROM public.identity AS identity_row
CROSS JOIN params
WHERE EXISTS (
    SELECT 1
    FROM jsonb_each_text(to_jsonb(identity_row)) AS field(key, value)
    WHERE field.value = params.email
);


/*
Step 2: Run this query on database ob_notification_uat.
Paste the account_id returned by Step 1 into params.account_id.
Change params.message_text when you want to find a different message.

The query always returns one row:
- status = FOUND and total_rows > 0 when messages exist
- status = ERROR and total_rows = 0 when no message exists
*/
WITH params AS (
    SELECT
        'PUT_ACCOUNT_ID_FROM_STEP_1_HERE'::text AS account_id,
        'Check your coupon details for eligible items'::text AS message_text
),
recipient_ids AS (
    SELECT DISTINCT
        recipient_row.id::text AS recipient_id
    FROM public.recipient AS recipient_row
    CROSS JOIN params
    WHERE recipient_row.account_id = params.account_id
       OR EXISTS (
            SELECT 1
            FROM jsonb_each_text(to_jsonb(recipient_row)) AS field(key, value)
            WHERE field.value = params.account_id
       )
),
matching_messages AS (
    SELECT message_row.*
    FROM public.message AS message_row
    CROSS JOIN params
    WHERE EXISTS (
        SELECT 1
        FROM recipient_ids
        WHERE message_row.recipient_id = recipient_ids.recipient_id
    )
      AND message_row.data::text ILIKE '%' || params.message_text || '%'
)
SELECT
    CASE
        WHEN COUNT(*) > 0 THEN 'FOUND'
        ELSE 'ERROR: notification message not found'
    END AS status,
    COUNT(*) AS total_rows,
    COALESCE(
        jsonb_agg(to_jsonb(matching_messages))
            FILTER (WHERE matching_messages.id IS NOT NULL),
        '[]'::jsonb
    ) AS data
FROM matching_messages;
