# SQL Class Notes — Session 2 (Subqueries, HAVING, CTEs, Window Functions, Frames)

> Instructor: Sumit Shukla | Dataset: same MySQL sample `employees` database as Session 1 (tables: `employees`, `salaries`, `department_employee`, `departments`)
> Continues from Session 1 notes (`sql_notes_session1.md`)

---

## 1. Subquery

**Explanation:**
A subquery is a query written **inside** another query. Instead of manually running a query to get a value (e.g., an average) and then hard-coding that value into a second query, you nest the first query directly inside the second — SQL evaluates the inner query first and feeds its result into the outer query.

**Example 1 — the "manual" (non-subquery) way, for comparison:**

```sql
-- Step 1: find the org-wide average salary (run separately, note the value, e.g. 63810)
SELECT AVG(salary)
FROM salaries
WHERE YEAR(to_date) = 9999;

-- Step 2: hard-code that value into a second query
SELECT *
FROM salaries
WHERE YEAR(to_date) = 9999
  AND salary > 63810;   -- hard-coded number from step 1
```

**Example 2 — the same logic as a subquery (no hard-coding):**

```sql
SELECT *
FROM salaries
WHERE YEAR(to_date) = 9999
  AND salary > (
        SELECT AVG(salary)
        FROM salaries
        WHERE YEAR(to_date) = 9999
      );
```

**Detail:** Both queries return the same result — employees earning more than the organization's average salary. The subquery version avoids hard-coding and stays correct even if the underlying data changes.

**Example 3 — subquery combined with JOIN + GROUP BY (find departments whose average salary beats the org average):**

```sql
SELECT A.department_number, AVG(B.salary)
FROM department_employee AS A
JOIN salaries AS B
  ON A.employee_number = B.employee_number
WHERE YEAR(A.to_date) = 9999
  AND YEAR(B.to_date) = 9999
GROUP BY A.department_number
HAVING AVG(B.salary) > (
    SELECT AVG(salary)
    FROM salaries
    WHERE YEAR(to_date) = 9999
);
```

---

## 2. HAVING

**Explanation:**
`WHERE` filters rows in the **original** (raw) table, **before** grouping. `HAVING` filters rows in a **GROUP BY result table**, i.e., it filters on aggregated values (like an average or count per group).

| Clause   | Filters...                    | Used with         |
| -------- | ----------------------------- | ----------------- |
| `WHERE`  | the original/raw table        | before `GROUP BY` |
| `HAVING` | the grouped/aggregated result | after `GROUP BY`  |

**Example 1 — filter groups by their aggregate value:**

```sql
SELECT A.department_number, AVG(B.salary) AS avg_sal
FROM department_employee AS A
JOIN salaries AS B
  ON A.employee_number = B.employee_number
WHERE YEAR(A.to_date) = 9999
  AND YEAR(B.to_date) = 9999
GROUP BY A.department_number
HAVING avg_sal > 65000;
```

**Example 2 — HAVING with a subquery (as in section 1, Example 3):**

```sql
... GROUP BY A.department_number
HAVING AVG(B.salary) > (SELECT AVG(salary) FROM salaries WHERE YEAR(to_date) = 9999);
```

**Result from class:** 3 departments had an average salary higher than the overall organization average.

---

## 3. CTE (Common Table Expression)

**Explanation:**
`CTE` = **Common Table Expression**. It's a way to write a subquery as a **named, reusable block** using `WITH ... AS (...)`, instead of nesting queries inside each other. It's officially part of the SQL standard (unlike ad-hoc subqueries, which are more of a workaround), and is generally **more efficient/performant** for complex, heavily-nested logic — especially valuable when you need to chain multiple steps (join → group → filter).

You can define **multiple CTEs** in one statement (comma-separated) and reference earlier CTEs from later ones, like chaining function calls.

**Example 1 — basic CTE (single step):**

```sql
WITH CTE1 AS (
    SELECT *
    FROM salaries
    WHERE YEAR(to_date) = 9999
)
SELECT * FROM CTE1;
```

**Example 2 — chaining multiple CTEs (join → filter → select clean columns):**

```sql
WITH CTE1 AS (
    SELECT A.employee_number, A.department_number, B.salary
    FROM department_employee AS A
    JOIN salaries AS B
      ON A.employee_number = B.employee_number
    WHERE YEAR(A.to_date) = 9999
      AND YEAR(B.to_date) = 9999
)
SELECT * FROM CTE1;
```

**Detail:** CTEs **cannot have duplicate column names** in their output. In this example, both `department_employee` and `salaries` have `from_date`/`to_date` columns, so you must explicitly select only the needed columns (rather than `SELECT *`) to avoid a naming clash.

**Example 3 — full chain: join → group by → filter (rewriting the subquery example as CTEs):**

```sql
WITH CTE1 AS (
    SELECT A.employee_number, A.department_number, B.salary
    FROM department_employee AS A
    JOIN salaries AS B
      ON A.employee_number = B.employee_number
    WHERE YEAR(A.to_date) = 9999
      AND YEAR(B.to_date) = 9999
),
CTE2 AS (
    SELECT department_number, AVG(salary) AS avg_sal
    FROM CTE1
    GROUP BY department_number
)
SELECT *
FROM CTE2
WHERE avg_sal > (SELECT AVG(salary) FROM salaries WHERE YEAR(to_date) = 9999);
```

**Example 4 — adding a 3rd CTE to bring in the department name via another join:**

```sql
WITH CTE1 AS (
    SELECT A.employee_number, A.department_number, B.salary
    FROM department_employee AS A
    JOIN salaries AS B
      ON A.employee_number = B.employee_number
    WHERE YEAR(A.to_date) = 9999
      AND YEAR(B.to_date) = 9999
),
CTE2 AS (
    SELECT A.employee_number, A.salary, B.department_name
    FROM CTE1 AS A
    JOIN departments AS B
      ON A.department_number = B.department_number
)
SELECT * FROM CTE2;
```

**Other details:**

- Execution order of a CTE chain: SQL starts from the **final/outer SELECT**, sees it references a CTE, jumps back to execute that CTE (and any CTE _that_ one depends on) first, then feeds the result forward — even though CTEs are _written_ top-to-bottom, execution effectively works backward from the final query and resolves dependencies first.
- Filtering can be done **inside the `ON` clause of a JOIN** instead of a separate `WHERE` afterward — this is faster because rows are excluded _while_ joining rather than joined first and filtered after.

```sql
-- filtering inside ON instead of a separate WHERE
SELECT A.employee_number, CONCAT(B.first_name, ' ', B.last_name) AS full_name, C.salary, A.department_number
FROM department_employee AS A
JOIN employees AS B
  ON A.employee_number = B.employee_number
JOIN salaries AS C
  ON B.employee_number = C.employee_number
  AND YEAR(A.to_date) = 9999
  AND YEAR(C.to_date) = 9999;
```

- Nothing that happens during a query (CTE, window function, JOIN, etc.) modifies the actual table in the database — everything is processed **temporarily in RAM** (on the server) and discarded once the result is returned, unless you explicitly persist it (e.g., save to a new table/file).

---

## 4. Window Functions (OVER / PARTITION BY)

**Explanation:**
Regular `GROUP BY` **collapses** the table — you lose the original rows and get one row per group, reducing the table's cardinality (row/column count). A **window function** lets you compute an aggregate (like an average) **per group** while keeping **every original row** — the aggregate value is repeated alongside each row instead of collapsing them.

Process (conceptually, 2 steps):

1. **Partition** the data — split rows into groups (windows) based on a column (e.g., `department_number`).
2. **Apply an aggregation function** to each partition/window, and attach that result to every row in the partition.

**Syntax:**

```sql
SELECT *, AGG_FUNC(column) OVER (PARTITION BY grouping_column) AS alias_name
FROM table_name;
```

**Example 1 — department-wise average salary, keeping every row (no collapsing):**

```sql
SELECT *,
       AVG(salary) OVER (PARTITION BY department_number) AS avg_sal
FROM CTE1;
```

**Detail:** Compare to plain `GROUP BY`, which would instead return just one row per department (`department_number, avg_salary`) — losing the individual employee rows.

**Example 2 — window function used together with CTEs (typical real workflow):**

```sql
WITH CTE1 AS (
    SELECT A.employee_number,
           CONCAT(B.first_name, ' ', B.last_name) AS full_name,
           C.salary,
           A.department_number
    FROM department_employee AS A
    JOIN employees AS B
      ON A.employee_number = B.employee_number
    JOIN salaries AS C
      ON B.employee_number = C.employee_number
      AND YEAR(A.to_date) = 9999
      AND YEAR(C.to_date) = 9999
)
SELECT *,
       AVG(salary) OVER (PARTITION BY department_number) AS avg_sal
FROM CTE1;
```

**Example 3 — using a window-function CTE + outer filter to find employees earning above their own department's average (no separate GROUP BY + JOIN needed):**

```sql
WITH CTE1 AS ( ... ),  -- same as Example 2
CTE2 AS (
    SELECT *,
           AVG(salary) OVER (PARTITION BY department_number) AS avg_sal
    FROM CTE1
)
SELECT *
FROM CTE2
WHERE salary > avg_sal;
```

**Why use a window function instead of subquery/JOIN here?** Doing this with a subquery would require a **two-step process**: first aggregate department averages, then join that result back to the original table — more processing cost. A window function does both in one pass, without collapsing/re-joining.

**Other detail — real-world use case:** Finding "employees earning more than their department's average" is a classic window-function use case, since it needs a per-row comparison against a group-level aggregate.

---

## 5. Ranking Functions: RANK, DENSE_RANK, ROW_NUMBER

**Explanation:**
Ranking functions are window functions used to **order/rank rows within each partition**. They require `PARTITION BY` (to define the groups) and `ORDER BY` (to define the ranking order) inside `OVER(...)`.

| Function       | Behavior on ties                                                              |
| -------------- | ----------------------------------------------------------------------------- |
| `RANK()`       | Ties get the same rank; the **next rank is skipped** (e.g., 1, 2, 2, 4)       |
| `DENSE_RANK()` | Ties get the same rank; **no ranks are skipped** (e.g., 1, 2, 2, 3)           |
| `ROW_NUMBER()` | Every row gets a unique, sequential number regardless of ties (1, 2, 3, 4...) |

**Example 1 — rank employees by salary within each department (highest first):**

```sql
SELECT *,
       RANK() OVER (PARTITION BY department_number ORDER BY salary DESC) AS rnk
FROM CTE1;
```

**Detail:** Column alias cannot be named `rank` since `RANK` is a reserved function name — use something like `rnk`.

**Example 2 — find the single highest-paid employee in each department (rank = 1):**

```sql
WITH CTE1 AS ( ... ),  -- base data
CTE2 AS (
    SELECT *,
           RANK() OVER (PARTITION BY department_number ORDER BY salary DESC) AS rnk
    FROM CTE1
)
SELECT *
FROM CTE2
WHERE rnk = 1;
```

**Example 3 — comparing RANK vs DENSE_RANK vs ROW_NUMBER side by side:**

```sql
SELECT *,
       RANK()       OVER (PARTITION BY department_number ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY department_number ORDER BY salary DESC) AS dense_rnk,
       ROW_NUMBER() OVER (PARTITION BY department_number ORDER BY salary DESC) AS row_num
FROM CTE1;
```

**Worked illustration (one partition with salaries producing ties):**

```
Values (descending):  100  80   80   70   50
RANK():                1    2    2    4    5
DENSE_RANK():           1    2    2    3    4
ROW_NUMBER():           1    2    3    4    5
```

**Other detail:** Which ranking to use is a **business/organizational choice**, not a hard rule — e.g., "always use DENSE_RANK to rank our products" is a company convention. A benefit of `RANK` (with skipping) is that the **maximum rank value tells you the total count** of ranked items directly.

---

## 6. Frames (ROWS BETWEEN) — Moving Window / Moving Average

**Explanation:**
A **frame** is a sub-window that **moves within a partition/window**, with a fixed width you define in code — used for things like **moving averages** (typically over time-based data, e.g., year/month). Contrast with `PARTITION BY`, which is a fixed bucket; a frame slides row by row within that bucket (or within the whole table if there's no partition).

If the entire table is treated as **one window** (no `PARTITION BY`), you **must still use `ORDER BY`** — without it, the frame won't activate/make sense, since a frame relies on a defined row sequence.

**Frame boundary keywords:**
| Keyword | Meaning |
|---|---|
| `UNBOUNDED PRECEDING` | from the very first row up to the current row |
| `UNBOUNDED FOLLOWING` | from the current row to the very last row |
| `N PRECEDING` | N rows before the current row |
| `N FOLLOWING` | N rows after the current row |
| `CURRENT ROW` | the row currently being evaluated |

**Syntax:**

```sql
AGG_FUNC(column) OVER (
    [PARTITION BY col]
    ORDER BY col
    ROWS BETWEEN <start_boundary> AND <end_boundary>
) AS alias
```

**Detail on order:** boundaries are always written as `ROWS BETWEEN <earlier_boundary> AND <later_boundary>` — e.g., write `1 PRECEDING AND CURRENT ROW`, not the reverse.

**Example 1 — average from the very start through the current row:**

```sql
SELECT *,
       AVG(salary) OVER (
           ORDER BY department_number
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS f1
FROM CTE1;
```

**Example 2 — average from the current row to the very end:**

```sql
SELECT *,
       AVG(salary) OVER (
           ORDER BY department_number
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS f2
FROM CTE1;
```

**Example 3 — a small moving average: 1 row before + current row:**

```sql
SELECT *,
       AVG(salary) OVER (
           ORDER BY department_number
           ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
       ) AS f3
FROM CTE1;
```

**Example 4 — a small moving average: current row + 1 row after:**

```sql
SELECT *,
       AVG(salary) OVER (
           ORDER BY department_number
           ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING
       ) AS f4
FROM CTE1;
```

**Other details:**

- No `PARTITION BY` was used in the frame examples because the instructor treated the **entire table as a single window/partition**. If you _do_ partition (e.g., `PARTITION BY department_number`), the frame's moving-average calculation restarts fresh at each new partition boundary.
- Moving averages generally make the most sense on **time-ordered data** (e.g., `ORDER BY year, month`); the class used `department_number` only to illustrate the mechanics.

---

## 7. Clause / Concept Quick Reference (Session 2 additions)

```sql
-- Subquery
SELECT * FROM t WHERE col > (SELECT AVG(col) FROM t);

-- HAVING (filters grouped results)
SELECT g, AVG(col) FROM t GROUP BY g HAVING AVG(col) > 100;

-- CTE (chainable, named subqueries)
WITH CTE1 AS (...), CTE2 AS (SELECT * FROM CTE1 ...)
SELECT * FROM CTE2;

-- Window function (aggregate without collapsing rows)
SELECT *, AGG(col) OVER (PARTITION BY g) AS alias FROM t;

-- Ranking within partitions
SELECT *, RANK() OVER (PARTITION BY g ORDER BY col DESC) AS rnk FROM t;

-- Frame (moving window)
SELECT *, AGG(col) OVER (ORDER BY g ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS f FROM t;
```

---

## 8. Topics Mentioned but Not Covered in Detail This Session

- `LEAD` / `LAG` window functions (referenced by a student as being in the practice sheet, not taught live)
- Indexing / performance optimization
- Deeper schema design

> Instructor note: next session (Tuesday) starts a new topic — practice this session's material (subqueries, CTEs, window functions, ranking, frames) beforehand.
