# SQL Class Notes — Session 1 (Basics: RDBMS, WHERE, GROUP BY, JOINs)

> Instructor: Sumit Shukla | Dataset: MySQL sample `employees` database (tables: `employees`, `salaries`, `titles`, `dept_employee`, `departments`, `dept_manager`)

---

## 1. Why SQL / What is a Database

**Explanation:**
Organizations (e.g., Zomato) collect large amounts of data (user data from customers/restaurant owners/delivery partners, plus orders data). This data can't live in flat files/Excel — it needs to be organized and queryable at scale. Companies rent space (a **data center**) from providers like Google, Microsoft, or Zoho (similar to renting a hotel room). Inside that rented space, the organization creates **databases** (like folders on a hard drive), and inside each database, data is stored as **tables** (rows and columns).

- **Table** = rows (records) + columns (fields)
- **Relationship** = a common column connecting two tables (e.g., `department_id` links `departments` and `orders`)
- **RDBMS** (Relational Database Management System) = the full system with two components:
  - **Client** — the interface used to write/send queries (connects via ID, password, hostname, port)
  - **Server** — where the actual data + processing power (CPU/RAM) live
- The client sends only the **query** (not raw data) to the server; the server processes it and returns the **result**.

**Example (conceptual):**

```
Question: "How many orders were placed between 1st May 2026 and 21st May 2026?"
→ Cannot ask this in plain English (SQL is NOT an LLM)
→ Must convert into a SQL query and send via the client to the server
```

**Other details:**

- SQL = **S**tructured **Q**uery **L**anguage — a _communication_ language, not a programming language.
- MySQL, PostgreSQL, MS SQL Server are all **providers** of RDBMS software (like different coffee brands — core product is the same, minor "taste"/syntax differences).
- SQL syntax is ~99% same across providers; ~1% varies (e.g., `SELECT TOP` is MS SQL syntax, not MySQL).
- On-premise = you manage the entire infra yourself. Cloud = a provider manages the infra for you.
- Real-world practice: databases are often **replicated** — a primary database (untouched) and a mirror database (used for querying) to protect production data. Records of employees who leave are moved to a separate table via a **trigger**, not deleted from the active table.

---

## 2. SQL Basics (syntax rules)

**Explanation:**

- SQL is **case-insensitive** (keywords and, in MySQL, even data can be case-insensitive — varies by platform).
- SQL is a **script language** — every query needs a **delimiter**, which is the semicolon `;` marking the end of a query.
- Comments are written with `--`.
- Run a query: `Ctrl + Enter` (Windows) or `Cmd + Return` (Mac).
- You must **activate/select** a database before querying its tables, using `USE`.

**Example:**

```sql
-- selecting the active database
USE employee;

-- this is a comment, SQL ignores this line
SELECT * FROM employees;
```

---

## 3. SELECT and LIMIT

**Explanation:**
`SELECT *` fetches all columns from a table. Since tables can be huge, `LIMIT` restricts the number of rows returned.

**Example 1 — select everything:**

```sql
SELECT * FROM employees;
```

**Example 2 — limit to first 10 rows:**

```sql
SELECT * FROM employees
LIMIT 10;
```

**Other detail:** `*` means "all columns/fields" for the given table.

---

## 4. Aggregation: COUNT

**Explanation:**
`COUNT` is an aggregation function.

- `COUNT(column_name)` — counts non-null values in that column only.
- `COUNT(*)` — counts every row/record (regardless of nulls in individual columns).
- `COUNT(DISTINCT column_name)` — counts unique non-null values.

**Example 1 — count a specific column:**

```sql
SELECT COUNT(employee_number)
FROM employees;
```

**Example 2 — count all rows:**

```sql
SELECT COUNT(*)
FROM employees;
```

**Example 3 — count unique values:**

```sql
SELECT COUNT(DISTINCT employee_number)
FROM employees;
```

**Other detail:** If a row's value for a counted column is `NULL`, that row is excluded from `COUNT(column_name)` but still included in `COUNT(*)`. A **primary key** column (e.g., `department_id` in `departments`) can never be null or duplicated, so `COUNT(*)` = `COUNT(DISTINCT ...)` on such tables.

---

## 5. Filtering with WHERE

**Explanation:**
`WHERE` filters rows based on a condition. Clause order matters: `SELECT → FROM → WHERE → LIMIT`. Multiple conditions are combined with `AND` / `OR`. Note: SQL uses a single `=` for equality (unlike Python's `==`).

**Example 1 — single condition:**

```sql
SELECT * FROM employees
WHERE gender = 'M';
```

**Example 2 — range condition (AND):**

```sql
SELECT * FROM salaries
WHERE salary > 10000 AND salary < 50000
LIMIT 10;
```

**Example 3 — filter + aggregate:**

```sql
SELECT COUNT(*) FROM employees
WHERE gender = 'F';
```

**Example 4 — filtering on a date's year using YEAR():**

```sql
-- find rows where the "to_date" year is 9999 (i.e., the still-active / latest record)
SELECT * FROM salaries
WHERE YEAR(to_date) = 9999;
```

**Detail:** In this sample dataset, an "open-ended" record (still current) is stored with `to_date = 9999-01-01` instead of `NULL`, since SQL columns are often not allowed to be null. This is a common pattern to detect "current/latest" records.

---

## 6. Pattern Matching with LIKE

**Explanation:**
`LIKE` filters text using wildcard patterns:

- `%` = any number of characters (including zero)
- `_` = exactly one character

| Pattern   | Meaning                                                      |
| --------- | ------------------------------------------------------------ |
| `'A%'`    | starts with A                                                |
| `'%A'`    | ends with A                                                  |
| `'%A%'`   | contains A anywhere                                          |
| `'__A%'`  | A is the 3rd character, followed by any number of characters |
| `'__A__'` | exactly 5 characters total, with A as the 3rd character      |

**Example 1 — starts with A:**

```sql
SELECT * FROM employees
WHERE first_name LIKE 'A%';
```

**Example 2 — ends with A:**

```sql
SELECT * FROM employees
WHERE first_name LIKE '%A';
```

**Example 3 — 3rd letter is A, any length after:**

```sql
SELECT * FROM employees
WHERE first_name LIKE '__A%';
```

**Other detail:** MySQL's `LIKE` is case-insensitive by default (some other platforms, e.g., SQL Server, are case-sensitive).

---

## 7. Aggregation: AVG

**Explanation:**
`AVG(column)` computes the average/mean of a numeric column. (Note: `MEDIAN` and `SUM` do not compute an average — a common quiz mistake.)

**Example:**

```sql
SELECT AVG(salary)
FROM salaries
WHERE YEAR(to_date) = 9999;   -- current salary only
```

---

## 8. GROUP BY

**Explanation:**
`GROUP BY` groups rows by one or more columns so aggregate functions (COUNT, AVG, SUM, etc.) apply per group instead of the whole table. Rule: every non-aggregated column in `SELECT` must also appear in `GROUP BY`.

Clause order: `SELECT → FROM → WHERE → GROUP BY → ORDER BY → LIMIT` (this order never changes).

**Example 1 — average salary per department:**

```sql
SELECT department_id, AVG(salary)
FROM employee
GROUP BY department_id;
```

**Example 2 — group by multiple columns:**

```sql
SELECT department_id, gender, AVG(salary)
FROM employee
GROUP BY department_id, gender;
```

**Example 3 — filter before grouping (WHERE + GROUP BY):**

```sql
SELECT department_id, AVG(salary)
FROM employee
WHERE gender = 'M'
GROUP BY department_id;
```

**Example 4 — count of employees by gender:**

```sql
SELECT gender, COUNT(*)
FROM employees
GROUP BY gender;
```

**Other detail:** Before writing a GROUP BY query, first sketch what the **output table** should look like (which columns, what each row represents) — then write the query to match that shape.

---

## 9. JOINs

**Explanation:**
Used to combine data across multiple tables via a common column (relationship). Types:

| Join type                     | Returns                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------- |
| `INNER JOIN` (or just `JOIN`) | Only rows where the key **matches in both** tables                              |
| `LEFT JOIN`                   | All rows from the **left** table + matched rows from right (unmatched = `NULL`) |
| `RIGHT JOIN`                  | All rows from the **right** table + matched rows from left (unmatched = `NULL`) |
| `OUTER JOIN` (FULL)           | All rows from **both** tables, matched + unmatched (`NULL` where no match)      |

Syntax pattern:

```sql
SELECT *
FROM table1 AS A
JOIN table2 AS B
  ON A.common_column = B.common_column;
```

- Table written first (after `FROM`) = **left table**.
- `AS` gives an **alias** (nickname) so you don't repeat full table names.
- Plain `JOIN` = `INNER JOIN` by default in MySQL.
- Conditions can be added inside the `ON` clause with `AND` — this is more optimized than a separate `WHERE`, since filtering happens _while_ joining rather than after.

**Example 1 — basic two-table inner join:**

```sql
SELECT *
FROM emp AS A
INNER JOIN dept AS B
  ON A.dpt_id = B.dpt_id;
```

**Example 2 — join salaries with dept_employee to get latest salary per current department:**

```sql
SELECT *
FROM salaries AS A
JOIN dept_employee AS B
  ON A.employee_number = B.employee_number
WHERE YEAR(A.to_date) = 9999
  AND YEAR(B.to_date) = 9999;
```

**Why filter on both tables' `to_date`?** An employee can have multiple salary records (over time) AND belong to multiple departments (over time). Filtering `to_date` = 9999 on _both_ tables ensures you get each employee's _current_ salary tied to their _current_ department.

**Example 3 — join + GROUP BY (department-wise average salary):**

```sql
SELECT B.dpt_number, AVG(A.salary)
FROM salaries AS A
JOIN dept_employee AS B
  ON A.employee_number = B.employee_number
WHERE YEAR(A.to_date) = 9999
  AND YEAR(B.to_date) = 9999
GROUP BY B.dpt_number;
```

**Example 4 — chaining 3 tables (employee name + department name):**

```sql
SELECT A.first_name, C.department
FROM employees AS A
JOIN dept_employee AS B
  ON A.emp_number = B.emp_number
JOIN departments AS C
  ON B.dpt_number = C.dpt_number
WHERE YEAR(B.to_date) = 9999;
```

**Detail:** Joins must be **chained sequentially** — you cannot join table A directly to table C in one `ON` clause if there's no direct relationship; you join A→B, then B→C (like connecting Lego blocks). Build these queries iteratively: join tables one pair at a time, verify output, then add filters, then add the final `SELECT` columns — don't try to write the whole query in one shot.

**Example 5 — join for a specific employee (from live quiz):**

```sql
SELECT B.department_name
FROM department_employee AS A
JOIN departments AS B
  ON A.department_number = B.department_number
WHERE YEAR(A.to_date) = 9999
  AND A.employee_number = 10007;
```

---

## 10. Practice Questions Worked in Class (with answers)

```sql
-- Q1: How many employees have gender = 'M'?
SELECT COUNT(*) FROM employees
WHERE gender = 'M';
-- Answer: 179973 (~180k)

-- Q2: How many employees were hired before year 1987?
SELECT COUNT(*) FROM employees
WHERE hire_date < '1987-01-01';
-- Answer: 171466

-- Q3: Current department name for employee_number = 10007
SELECT B.department_name
FROM department_employee AS A
JOIN departments AS B
  ON A.department_number = B.department_number
WHERE YEAR(A.to_date) = 9999
  AND A.employee_number = 10007;
-- Answer: Research

-- Q4: Highest salary ever recorded
SELECT MAX(salary) FROM salaries;
-- Answer: 158220

-- Q5: How many rows in titles have title = 'Senior Engineer' AND to_date = 9999 (current)?
SELECT COUNT(*) FROM titles
WHERE title = 'Senior Engineer'
  AND YEAR(to_date) = 9999;
-- Answer: 85939
```

**Detail:** Date literals must be written in the same format used by the SQL engine, e.g. `'1987-01-01'` (`YYYY-MM-DD`).

---

## 11. Clause Order Cheat Sheet

```sql
SELECT   column1, column2, AGG_FUNC(column3)
FROM     table_name
WHERE    condition                -- row-level filter, before grouping
GROUP BY column1, column2
ORDER BY column1                  -- sorting (mentioned, not detailed yet)
LIMIT    n;                       -- always last
```

This order is fixed and never changes.

---

## 12. Topics Not Yet Covered (planned for next session)

- Subqueries
- Window functions (e.g., `RANK`, `DENSE_RANK`)
- Indexing / performance optimization
- Schema design (deeper dive)

> Instructor note: next session (Saturday) will cover more advanced topics — practice basic `WHERE` / `GROUP BY` / `JOIN` queries beforehand.
