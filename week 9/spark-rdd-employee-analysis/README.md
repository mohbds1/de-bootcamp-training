# Spark RDD Employee Analysis

This project was developed as part of a Spark RDD lab using Apache Spark inside a Docker-based itversity environment.

The objective of the lab was to practice core RDD transformations and actions while working with semi-structured employee data.

---

# Technologies Used

- Apache Spark
- PySpark
- Docker
- Jupyter Notebook
- RDD API

---

# Project Overview

The dataset contains employee information such as:

- Employee ID
- Name
- Department
- Job Title
- Salary
- Location
- Hire Date
- Performance Rating
- Years of Experience

The project demonstrates how Spark RDD can be used for:

- Parsing raw text data
- Cleaning invalid records
- Aggregating data
- Performing distributed computations

---

# Dataset Issues

The dataset intentionally included several invalid records, such as:

- Empty rows
- Incorrect column formatting
- Corrupted salary values

Example:

```text
Legal Counsel145000
````

This caused column shifting problems during processing.

To solve this issue, additional validation and filtering logic were applied before performing transformations.

---

# Tasks Implemented

## Task 1 — Parse Text Data

The raw CSV text data was converted into structured lists using:

```python
split(",")
```

---

## Task 2 — Count Name Occurrences

Used:

* map()
* reduceByKey()

to calculate how many times each employee name appeared.

---

## Task 3 — Filter Invalid Records

Invalid rows were filtered safely by checking:

* Column count
* Salary format validity

This step prevented Spark runtime errors during transformations.

---

## Task 4 — Average Salary Per Department

Calculated the average salary for each department using:

* map()
* reduceByKey()
* mapValues()

---

## Task 5 — Employee Count Per Department

Calculated the number of employees in each department using RDD aggregations.

---

# Key Spark Concepts Practiced

* RDD Transformations
* RDD Actions
* Distributed Processing
* Data Cleaning
* Aggregation
* Functional Programming with Lambda Expressions

---

# Project Structure

```text
spark-rdd-employee-analysis/
│
├── data/
│   └── employees.txt
│
├── employee_rdd_analysis.ipynb
│
└── README.md
```

---

# Final Notes

This lab helped strengthen my understanding of Apache Spark RDD operations and how distributed data processing works in practice.

It also demonstrated the importance of validating and cleaning raw data before applying transformations.