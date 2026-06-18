# PySpark Structured Streaming Labs

## 📖 Overview

This repository contains data processing using **Apache Spark (PySpark) Structured Streaming**. It demonstrates the implementation of end-to-end streaming pipelines, handling data ingestion, windowed aggregations, late-arriving data management, and writing to multiple storage sinks simultaneously.

## 🛠️ Environment & Tech Stack

The Assignments utilizes a self-contained containerized environment for seamless execution and testing:

* **Framework:** Apache Spark (PySpark Structured Streaming)
* **Environment:** Docker & Docker Compose (`itversity/itvdelab` image)
* **IDE:** Jupyter Notebook
* **Data Formats:** JSON, CSV, Parquet
* **Storage Sinks:** Local Filesystem and Local Hive Metastore (Derby)

## 📂 Repository Structure

```text
📦 spark-structured-streaming
 ┣ 📜 docker-compose.yml                       # Docker environment configuration
 ┣ 📓 Mohammed_Lab1_Spark_Structured_Streaming.ipynb # Lab 1: Basics of CSV Streaming
 ┣ 📓 Mohammed_Lab2_Temperature_Streaming.ipynb      # Lab 2: JSON Streaming, Windows & Watermarks
 ┣ 📂 Screenshots                              # Execution screenshots validating the output
 ┣ 📂 data                                     # Data storage directory (Mounted to container)
 ┃ ┣ 📂 json/                                  # Input stream source for Lab 2 (batch1 to batch6)
 ┃ ┣ 📂 csv/                                   # Input stream source for Lab 1 
 ┃ ┣ 📂 output/                                # Target sink for Parquet files
 ┃ ┣ 📂 spark-warehouse/                       # Hive table storage
 ┃ ┣ 📂 metastore_db/                          # Local Derby database for Hive metadata
 ┃ ┗ 📂 checkpoint/                            # Spark streaming checkpointing state

```

## 🔬 Lab Details

### Lab 1: Streaming Basics (CSV)

* **Objective:** Read streaming data from a directory of CSV files.
* **Concepts Covered:** Defining schemas for streaming data, basic transformations, and writing streams to standard outputs.

### Lab 2: Temperature Streaming (JSON & Windowing)

* **Objective:** Read a live stream of temperature readings from JSON files and calculate the average temperature per country every 15 minutes.
* **Concepts Covered:**
* **Event-Time Processing:** Utilizing the `event_timestamp` to process records based on when they occurred.
* **Windowing:** Grouping data into 15-minute tumbling windows.
* **Watermarking:** Handling late-arriving data by implementing a 10-minute watermark delay threshold.
* **Multi-Sink Output:** Utilizing `foreachBatch` to write micro-batches to **both** a filesystem (as Parquet files) and a structured Hive table simultaneously.
* **Append Mode:** Ensuring proper output modes are used for windowed aggregations saved to file-based sinks.

## 🚀 How to Run the Project

**1. Start the Docker Environment:**
Open your terminal in the project root directory and run:

```bash
docker-compose up -d

```

**2. Access Jupyter Notebook:**
Execute into the container and start the notebook server:

```bash
docker exec -it itvdelab_assignment bash
jupyter notebook --ip=0.0.0.0 --port=8889 --no-browser --allow-root

```

*Copy the generated URL (with the token) and paste it into your web browser.*

**3. Run the Streaming Pipeline (Lab 2):**

* Open `Mohammed_Lab2_Temperature_Streaming.ipynb`.
* Clear any existing files in `data/json/`, `data/checkpoint/`, and `data/output/`.
* Run the notebook cells sequentially up to the `.awaitTermination()` cell to start the streaming engine.

**4. Simulate the Data Stream:**

* Slowly drop `batch1.json` through `batch6.json` into the `data/json/` directory one by one (waiting a few seconds between each).
* *Note: The aggregated data is pushed to the output sinks once the event time crosses the 10-minute watermark threshold.*

**5. Verify the Output:**

* Stop the streaming cell.
* Run the final evaluation cells to query the generated Parquet files and the Hive table.

## 🧹 Cleanup

To stop and remove the container, run:

```bash
docker-compose down

```

*(Optional) Add `-v` to remove mounted volumes and clear all generated metadata.*
