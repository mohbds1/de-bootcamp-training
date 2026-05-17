# Required Architecture

```text
+--------------------------------------------------+
|          Python Streaming Generator              |
|  Generates continuous logistics CSV data files   |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|               CSV Streaming Data                 |
|     Real-time CSV files written to input dir     |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|                  Apache NiFi                     |
|        File ingestion and stream orchestration   |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|               64 KB File Chunking                |
|      SplitText processor for scalable chunks     |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|            CSV to JSON Transformation            |
|   Schema validation + ConvertRecord processors   |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|                  Apache Kafka                    |
|     Distributed streaming topic: logistics-clean |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|             Apache NiFi Consumer                 |
|      ConsumeKafkaRecord_2_6 processor layer      |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|                       HDFS                       |
|     Partitioned distributed JSON data storage    |
|   /data/year=YYYY/month=MM/day=DD/              |
+--------------------------------------------------+
```