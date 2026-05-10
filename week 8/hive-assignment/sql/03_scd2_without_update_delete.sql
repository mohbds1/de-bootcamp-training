set hive.execution.engine=mr;
set mapreduce.framework.name=local;

DROP TABLE IF EXISTS customer_dim;
DROP TABLE IF EXISTS customer_stage;
DROP TABLE IF EXISTS customer_dim_new;

CREATE EXTERNAL TABLE customer_dim (
    customer_id   STRING,
    name          STRING,
    email         STRING,
    phone_number  STRING,
    address       STRING,
    join_date     STRING,
    start_date    STRING,
    end_date      STRING,
    is_current    STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\"",
    "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/customer/scd2_source'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE customer_stage (
    customer_id   STRING,
    name          STRING,
    email         STRING,
    phone_number  STRING,
    address       STRING,
    join_date     STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\"",
    "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/customer/updated'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE customer_dim_new (
    customer_id   STRING,
    name          STRING,
    email         STRING,
    phone_number  STRING,
    address       STRING,
    join_date     STRING,
    start_date    STRING,
    end_date      STRING,
    is_current    STRING
)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE customer_dim_new

-- 1) keep old historical records
SELECT
    d.customer_id,
    d.name,
    d.email,
    d.phone_number,
    d.address,
    d.join_date,
    d.start_date,
    d.end_date,
    d.is_current
FROM customer_dim d
WHERE d.is_current = '0'

UNION ALL

-- 2) keep current records that did not change
SELECT
    d.customer_id,
    d.name,
    d.email,
    d.phone_number,
    d.address,
    d.join_date,
    d.start_date,
    d.end_date,
    d.is_current
FROM customer_dim d
LEFT JOIN customer_stage s
    ON d.customer_id = s.customer_id
WHERE d.is_current = '1'
  AND (
        s.customer_id IS NULL
        OR (
            d.name         = s.name
            AND d.email   = s.email
            AND d.phone_number = s.phone_number
            AND d.address = s.address
        )
  )

UNION ALL

-- 3) expire changed current records
SELECT
    d.customer_id,
    d.name,
    d.email,
    d.phone_number,
    d.address,
    d.join_date,
    d.start_date,
    date_format(current_date(), 'yyyy-MM-dd') AS end_date,
    '0' AS is_current
FROM customer_dim d
JOIN customer_stage s
    ON d.customer_id = s.customer_id
WHERE d.is_current = '1'
  AND (
        d.name <> s.name
        OR d.email <> s.email
        OR d.phone_number <> s.phone_number
        OR d.address <> s.address
  )

UNION ALL

-- 4) insert new customers and new versions of changed customers
SELECT
    s.customer_id,
    s.name,
    s.email,
    s.phone_number,
    s.address,
    s.join_date,
    date_format(current_date(), 'yyyy-MM-dd') AS start_date,
    NULL AS end_date,
    '1' AS is_current
FROM customer_stage s
LEFT JOIN customer_dim d
    ON s.customer_id = d.customer_id
   AND d.is_current = '1'
WHERE d.customer_id IS NULL
   OR (
        d.name <> s.name
        OR d.email <> s.email
        OR d.phone_number <> s.phone_number
        OR d.address <> s.address
   );

INSERT OVERWRITE DIRECTORY '/user/hive/output/customer_scd2_mixed'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT *
FROM customer_dim_new;

SELECT *
FROM customer_dim_new
ORDER BY customer_id, start_date;