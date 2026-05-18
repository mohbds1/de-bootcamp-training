# 🚀 Week 9: Distributed Data Processing and Real-Time Streaming Pipelines

Welcome to the **Week 9** repository of the Data Engineering Bootcamp.

This week focuses on advanced Big Data Engineering concepts using distributed processing and real-time streaming technologies such as:

- Apache Spark
- PySpark
- Apache Kafka
- Apache NiFi
- Hadoop HDFS
- Docker

The projects in this repository demonstrate both batch-oriented distributed computation and enterprise-grade real-time streaming architectures commonly used in modern data platforms.

---

# 📂 Projects Showcase

## 1. ⚡ Spark DataFrame Practice (`spark-assignment`)

A hands-on Apache Spark project focused on understanding and practicing PySpark DataFrame operations.

### 📌 Objective

Learn how Spark DataFrames are created, inspected, cleaned, transformed, and joined while working with structured datasets inside a distributed Spark environment.

### 🧠 Key Concepts Covered

- SparkSession
- DataFrame Operations
- Schema Inspection
- Filtering and Selection
- Column Transformations
- Null Handling
- Duplicate Removal
- Aggregations
- Joins
- Data Validation

### 📓 Included Notebooks

- `01_spark_dataframe_basics.ipynb`
- `02_dataframe_transformations.ipynb`

### 🛠️ Technologies Used

- Apache Spark
- PySpark
- Docker
- Jupyter Notebook

---

## 2. 👨‍💼 Spark RDD Employee Analysis (`spark-rdd-employee-analysis`)

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

## 3. 🚚 Real-Time Logistics Data Pipeline (`real-time-logistics-data-pipeline`)

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

# 🧱 Week 9 Engineering Focus

This week combines multiple Big Data Engineering paradigms:

* Distributed Batch Processing
* Distributed DataFrames
* Low-Level RDD APIs
* Real-Time Stream Processing
* Distributed Storage Systems

to simulate real-world enterprise data engineering architectures.

---

# 📚 Learning Outcomes

By completing these projects, the following practical skills were developed:

* Building distributed Spark pipelines
* Working with Spark DataFrames
* Using low-level RDD APIs
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
├── spark-assignment/
│
├── spark-rdd-employee-analysis/
│
├── real-time-logistics-data-pipeline/
│
└── README.md
```

---

# 🌟 Final Notes

This week provided practical exposure to both distributed batch analytics and real-time streaming systems.

The projects focused not only on writing code, but also on understanding scalability, reliability, data validation, distributed processing behavior, and enterprise-level pipeline design.

---

*Feel free to explore each project directory for notebooks, pipeline configurations, technical documentation, screenshots, and implementation details.*
