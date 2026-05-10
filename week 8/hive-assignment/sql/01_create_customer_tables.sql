set hive.execution.engine=mr;
set mapreduce.framework.name=local;

DROP TABLE IF EXISTS ext_customer;
DROP TABLE IF EXISTS int_customer;

CREATE EXTERNAL TABLE ext_customer (
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

CREATE TABLE int_customer (
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
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE int_customer
SELECT * FROM ext_customer;

SELECT * FROM ext_customer LIMIT 10;
SELECT * FROM int_customer LIMIT 10;