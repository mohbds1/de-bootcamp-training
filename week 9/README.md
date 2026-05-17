# 🚀 Week 9: Distributed Data Processing and Real-Time Streaming Pipelines

Welcome to the **Week 9** repository of the Data Engineering Bootcamp.

This week focuses on advanced Big Data Engineering concepts using:

- Apache Spark
- Apache Kafka
- Apache NiFi
- Hadoop HDFS
- Distributed Streaming Architectures

The projects in this repository demonstrate both batch-oriented distributed computation and real-time streaming data pipelines commonly used in modern enterprise data platforms.

---

# 📂 Projects Showcase

## 1. ⚡ Spark RDD Employee Analysis (`spark-rdd-employee-analysis`)

A distributed data processing project built using Apache Spark RDD APIs inside a Docker-based Spark environment.

### 📌 Objective

Practice low-level Spark RDD transformations and actions while processing semi-structured employee datasets containing invalid and corrupted records.

### 🧠 Key Concepts Covered

- RDD Transformations
- RDD Actions
- Distributed Processing
- Data Cleaning
- Aggregation
- Functional Programming with PySpark
- Fault-Tolerant Data Processing

### ⚙️ Implemented Tasks

- Parsing raw text records
- Filtering malformed rows
- Salary aggregation
- Department-level analytics
- Employee count calculations
- Average salary computation

### 🛠️ Technologies Used

- Apache Spark
- PySpark
- Docker
- Jupyter Notebook

---

## 2. 🚚 Real-Time Logistics Data Pipeline (`real-time-logistics-data-pipeline`)

A complete real-time streaming architecture built using Apache NiFi, Apache Kafka, and Hadoop HDFS.

### 📌 Objective

Design and implement a scalable streaming pipeline capable of ingesting, transforming, validating, streaming, and storing logistics telemetry data in near real-time.

### 🧠 Key Concepts Covered

- Streaming ETL Pipelines
- Kafka Event Streaming
- Schema Validation
- CSV to JSON Transformation
- HDFS Distributed Storage
- File Chunking
- Monitoring & Reliability
- Back Pressure & Retry Handling
- Failure Routing

### ⚙️ Pipeline Architecture

```text
Python Streaming Generator
        ↓
CSV Streaming Files
        ↓
Apache NiFi
        ↓
64 KB File Chunking
        ↓
CSV to JSON Transformation
        ↓
Apache Kafka
        ↓
Apache NiFi Consumer
        ↓
HDFS
````

### 🛠️ Technologies Used

* Python
* Apache NiFi
* Apache Kafka
* Hadoop HDFS
* Docker & Docker Compose

---

# 🧱 Week 9 Architecture Focus

This week combines both:

* Distributed Batch Processing
* Real-Time Stream Processing

to simulate modern enterprise-grade data engineering systems.

---

# 📚 Learning Outcomes

By completing these projects, the following practical skills were developed:

* Building distributed Spark pipelines
* Designing real-time streaming architectures
* Handling corrupted streaming data
* Building scalable Kafka pipelines
* Integrating NiFi with HDFS
* Applying monitoring and reliability engineering concepts
* Managing distributed storage systems

---

# 🛠️ Core Technologies Used

* Apache Spark
* PySpark
* Apache Kafka
* Apache NiFi
* Hadoop HDFS
* Docker
* Python

---

# 📁 Repository Structure

```text
week 9/
│
├── spark-rdd-employee-analysis/
│
├── real-time-logistics-data-pipeline/
│
└── README.md
```

---

*Feel free to explore each project directory for notebooks, pipeline configurations, technical documentation, screenshots, and implementation details.*
