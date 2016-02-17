from django.db import connections

cursor = connection.cursor()
cursor.execute("""SELECT object_id, SUM(qty) AS sum_qty
FROM (
SELECT
    object_out_id as object_id
    ,-1 * qty as qty
    FROM
        bunker_flow AS flow1
UNION ALL
SELECT
    object_in_id as object_id
    ,qty
    FROM
        bunker_flow
) AS flow
GROUP BY
    object_id""")