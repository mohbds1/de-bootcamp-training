# HDFS Commands Used

## Start Hadoop Distributed File System

```bash
start-dfs.sh
```

---

## Verify Hadoop Services

```bash
jps
```

---

## Create Main Data Directories

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -mkdir -p /errors
```

---

## Create Date-Partitioned Storage Structure

```bash
hdfs dfs -mkdir -p /data/year=2026/month=05/day=17
```

---

## Set Directory Permissions

```bash
hdfs dfs -chmod -R 777 /data /errors
```

---

## Verify HDFS Structure

```bash
hdfs dfs -ls /
```

---

## View Partitioned Data Files

```bash
hdfs dfs -ls -R /data
```

---

## View Error Files

```bash
hdfs dfs -ls -R /errors
```

---

## Read JSON Files from HDFS

```bash
hdfs dfs -cat /data/year=2026/month=05/day=17/logistics_20260517_182206_0071be83-7ec1-4f6a-906b-056f19296f4d.json | head
```

---

## Read First Available File Automatically

```bash
hdfs dfs -cat $(hdfs dfs -ls /data/year=2026/month=05/day=17 | awk 'NR==2 {print $8}') | head
```

---

## Remove Old Test Data

```bash
hdfs dfs -rm -r /data/year=2026
```

---

## Verify HDFS Default Filesystem

```bash
hdfs getconf -confKey fs.defaultFS
```

---

## Restart HDFS Services

```bash
stop-dfs.sh
start-dfs.sh
```