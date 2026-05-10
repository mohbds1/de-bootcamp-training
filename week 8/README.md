# 🚀 Week 8: Big Data Processing and Data Ingestion Pipelines

Welcome to the **Week 8** repository of the Data Engineering Bootcamp.  
This week focuses on practical Big Data Engineering workflows using **Apache Hive**, **HDFS**, and **Apache NiFi** for building scalable data ingestion and processing pipelines.

The projects in this directory demonstrate real-world concepts in distributed data systems, ETL automation, and batch data processing.

---

# 📂 Projects Showcase

## 1. 🐘 Hive Data Warehouse Assignment (`hive-assignment`)

A hands-on Big Data project designed to demonstrate the use of Apache Hive for querying and managing large-scale datasets inside Hadoop ecosystems.

### 📌 Objective
Build and manage analytical tables using HiveQL while applying Data Warehouse concepts on distributed storage systems.

### 🧠 Key Concepts Covered
- Hive Database and Table Creation
- External and Managed Tables
- Data Loading into HDFS
- Partitioning and Query Optimization
- Aggregation and Analytical Queries
- HiveQL Transformations

### 🛠️ Technologies Used
- Apache Hive
- Hadoop HDFS
- HiveQL
- Linux

---

## 2. 🔄 NiFi Data Ingestion Pipeline (`Nifi-data-ingestion-pipeline`)

A complete ETL and Data Ingestion pipeline built using Apache NiFi to automate data movement between local storage and HDFS environments.

### 📌 Objective
Design a scalable and fault-tolerant ingestion pipeline capable of processing and transferring datasets into Hadoop storage systems.

### 🧠 Key Concepts Covered
- FlowFile Processing
- Processor Configuration
- Relationship Handling
- Retry and Penalization
- Back Pressure Configuration
- Incremental File Processing
- Modular Process Groups
- Data Routing and Monitoring

### ⚙️ Pipeline Workflow
1. Read incoming source files
2. Validate and transform records
3. Route success and failure relationships
4. Transfer processed data into HDFS
5. Monitor flow statistics and queue management

### 🛠️ Technologies Used
- Apache NiFi
- Hadoop HDFS
- JSON
- Linux Environment

---

# 🧱 Architecture Overview

This week combines multiple Big Data ecosystem components into one integrated workflow:

```text
Local Files
     │
     ▼
Apache NiFi
     │
     ▼
Data Validation & Transformation
     │
     ▼
HDFS Storage
     │
     ▼
Apache Hive
     │
     ▼
Analytical Queries & Reporting
````

---

# 📚 Learning Outcomes

By completing these projects, the following practical skills were developed:

* Building ETL pipelines using Apache NiFi
* Managing distributed storage with HDFS
* Writing analytical queries in HiveQL
* Understanding Data Warehouse workflows
* Handling large-scale data ingestion processes
* Applying Big Data Engineering best practices

---

# 🛠️ Core Technologies Used

* Apache Hive
* Apache NiFi
* Hadoop HDFS
* HiveQL
* Linux
* JSON

---

*Feel free to explore each project folder for implementation details, configurations, datasets, and screenshots.*