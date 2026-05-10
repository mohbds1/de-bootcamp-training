# Hive Customer Dimension Assignment

This project demonstrates the implementation of Apache Hive concepts in a Dockerized Hadoop environment.  
The assignment focuses on Hive table management, CSV parsing challenges, and implementing Slowly Changing Dimension Type 2 (SCD Type 2) without using transactional tables.

---

# Technologies Used

- Apache Hive
- Hadoop HDFS
- Docker
- PostgreSQL Metastore
- OpenCSVSerde

---

# Project Structure

```text
hive-assignment/
│
├── data/
│   ├── customer_scd2_mixed.csv
│   └── customer_updated.csv
│
├── output/
│   └── customer_scd2_mixed.csv
│
├── sql/
│   ├── 01_create_customer_tables.sql
│   ├── 02_drop_table_test.sql
│   └── 03_scd2_without_update_delete.sql
│
├── docker-compose.yml
└── README.md
````

---

# Assignment Tasks

The implementation covers the following requirements:

* Create internal and external Hive tables.
* Load CSV data into Hive tables.
* Solve delimiter issues inside address values without changing the CSV separator.
* Compare the behavior of internal and external tables after dropping them.
* Implement Slowly Changing Dimension Type 2 (SCD Type 2).
* Use `customer_updated.csv` to track customer changes.
* Implement SCD2 without using UPDATE or DELETE operations.

---

# Environment Setup

Start the environment:

```bash
docker compose up -d
```

Enter the container:

```bash
docker exec -it hive_assignment bash
```

Start HDFS:

```bash
start-dfs.sh
```

---

# Upload Data to HDFS

```bash
hdfs dfs -mkdir -p /user/hive/customer/scd2_source
hdfs dfs -mkdir -p /user/hive/customer/updated
hdfs dfs -mkdir -p /user/hive/output

hdfs dfs -put -f /opt/hive_data/customer_scd2_mixed.csv /user/hive/customer/scd2_source/
hdfs dfs -put -f /opt/hive_data/customer_updated.csv /user/hive/customer/updated/
```

---

# Running SQL Scripts

## 1. Create Internal & External Tables

```bash
hive -f /opt/hive_sql/01_create_customer_tables.sql
```

## 2. Drop Table Test

```bash
hive -f /opt/hive_sql/02_drop_table_test.sql
```

## 3. Run SCD Type 2 Logic

```bash
hive -f /opt/hive_sql/03_scd2_without_update_delete.sql
```

---

# CSV Delimiter Solution

The address column contained commas inside values, which caused Hive to incorrectly split rows.

To solve this problem, `OpenCSVSerde` was used with:

* `separatorChar`
* `quoteChar`
* `escapeChar`

This allowed Hive to correctly read quoted CSV values without modifying the original separator.

---

# SCD Type 2 Logic

The solution rebuilds the customer dimension using:

```sql
INSERT OVERWRITE
UNION ALL
```

instead of using UPDATE or DELETE operations.

The logic includes:

1. Keeping historical records.
2. Preserving unchanged current records.
3. Expiring changed records.
4. Inserting new and updated customer records.

---

# Final Output

The final processed file is generated in:

```text
output/customer_scd2_mixed.csv
```

The output contains:

* Active customer records
* Historical customer records
* Expired records
* Newly inserted records

---

# Notes

* External tables preserve raw files after DROP TABLE.
* Internal tables remove data and metadata together.
* Hive non-transactional tables require overwrite-based approaches for SCD2 implementations.
