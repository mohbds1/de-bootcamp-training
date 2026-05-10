# Real-Time Data Engineering Pipeline using Apache NiFi

## Project Overview

This project demonstrates the design and implementation of a real-time data engineering pipeline using Apache NiFi, PostgreSQL, Docker, and Hadoop HDFS.

The pipeline simulates a real-world streaming environment where data is collected from multiple sources, processed, cleaned, validated, transformed, and finally stored inside a distributed storage system (HDFS).

The project was built as a hands-on data engineering assignment to practice modern ETL and streaming concepts using open-source big data tools.

---

# Architecture

The pipeline is divided into five main layers:

## 1. Python Ingestion Layer

This layer generates semi-structured JSON transaction files continuously using a custom Python script.

The generated data intentionally includes:
- Missing IDs
- Invalid amount values
- Duplicate records
- Inconsistent status values

These issues are added intentionally to simulate dirty real-world datasets.

Apache NiFi monitors the input directory using:
- ListFile
- FetchFile

Processors.

---

## 2. API Ingestion Layer

This layer collects external real-time data from a public API using the NiFi `InvokeHTTP` processor.

The API used:
- Frankfurter Currency Exchange API

The retrieved market data is streamed directly into the pipeline for further processing and storage.

---

## 3. PostgreSQL Ingestion Layer

This layer demonstrates database ingestion using PostgreSQL.

NiFi connects to PostgreSQL and retrieves structured records which are integrated into the main pipeline.

This layer represents structured enterprise data sources commonly used in production environments.

---

## 4. Transformation Layer

This is the core processing layer of the pipeline.

Several transformations are applied:

### Data Validation
Records with:
- Missing IDs
- Invalid amount values

are filtered and routed separately.

### Data Cleaning
Ambiguous status values such as:
- ???

are replaced with standardized values.

### Data Type Conversion
The `amount` field is converted into numeric format for analytics compatibility.

### Deduplication
Duplicate records are removed using:
- DeduplicateRecord
- SHA-256 hashing

### Data Enrichment
Additional metadata such as NiFi processing timestamps are added to records.

---

## 5. HDFS Load Layer

The final cleaned datasets are stored inside Hadoop Distributed File System (HDFS).

NiFi processors used:
- MergeRecord
- PutHDFS

Data is stored in separate HDFS directories:
- `/user/itversity/transactions`
- `/user/itversity/market_data`

---

# Technologies Used

- Apache NiFi 2.9.0
- Hadoop HDFS
- Docker & Docker Compose
- PostgreSQL
- Python
- JSON
- Apache NiFi Record Processors

---

# Docker Services

The environment contains the following containers:

| Service | Purpose |
|---|---|
| nifi | Main orchestration and ETL engine |
| postgres_db | Relational database source |
| itvdelab | Hadoop and HDFS environment |

---

# Key Features

- Real-time file ingestion
- API data ingestion
- Database ingestion
- Data cleaning and validation
- Duplicate detection
- Distributed storage using HDFS
- Modular NiFi architecture
- Multi-source streaming pipeline

---

# Project Structure

```text
.
├── data/
│   └── input/
├── custom_nars/
├── jdbc_drivers/
├── postgres_data/
├── data_generator.py
├── postgres_setup.sql
├── docker-compose.yaml
├── nifi_pipeline.json
└── README.md
````

---

# How to Run

## 1. Start Docker Containers

```bash
docker compose up -d
```

## 2. Open NiFi

```text
https://localhost:8443
```

## 3. Run the Python Generator

```bash
python data_generator.py
```

## 4. Start the NiFi Flow

Enable all processors and process groups from the NiFi UI.

---

# Learning Outcomes

This project helped in understanding:

* Stream processing concepts
* ETL pipeline design
* Record-based processing in NiFi
* Data quality handling
* HDFS integration
* Real-time ingestion architecture
* Distributed data storage