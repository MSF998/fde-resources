### Introduction to Pandas & Import

**Explanation:** Pandas (Panel Data) is a core Python library for structured data analysis, functioning as an alternative to Excel capable of processing millions of records without lag. By industry convention, it is imported using the alias `pd`.[cite: 1]
**Example Code:**

```python
import pandas as pd
```

---

### Loading Data into DataFrames

**Explanation:** To process data in Pandas, it must be loaded into a recognized container called a DataFrame. The `pd.read_csv()` method imports CSV file sources into this structure.[cite: 1]
**Example Code:**

```python
df = pd.read_csv("content/churn_data.csv")
```

---

### Sanity Check Methods & Attributes

**Explanation:** Pandas provides quick attributes (without parentheses) and methods (with parentheses) to explore the structure and contents of a loaded DataFrame:[cite: 1]

- `head(n)` / `tail(n)`: Returns the top/bottom `n` rows (defaults to 5).[cite: 1]
- `info()`: Provides a complete snapshot including data types, non-null counts, and memory usage.[cite: 1]
- `shape`: Returns a tuple showing `(number of rows, number of columns)`.[cite: 1]
- `columns`: Returns a list of all column headers.[cite: 1]
- `index`: Returns row index limits and step size.[cite: 1]

**Example Code:**

```python
df.head(10)  # Top 10 rows
df.tail()    # Bottom 5 rows
df.info()    # Data frame snapshot
df.shape     # Rows and columns count
df.columns   # Column names
```

---

### Slicing and Fetching Columns

**Explanation:** Retrieve columns by indexing the DataFrame with square brackets. Providing a single string fetches one column as a Series. To fetch multiple columns, you must pass them as a list (using double square brackets).[cite: 1]
**Example Code:**

```python

# Fetching a single column

df['churn']

# Fetching multiple columns

df[['customerID', 'tenure']]
```

---

### Filtering Data with Single Conditions

**Explanation:** Filtering is achieved by creating a boolean series using a comparison operator (`==`, `<`, `>`, etc.) and passing it as an index to the DataFrame. This returns only the rows where the condition evaluates to `True`.[cite: 1]
**Example Code:**

```python

# Filter out customers who churned

condition = df['churn'] == 'yes'
filtered_df = df[condition]
```

---

### Filtering with Multiple Conditions

**Explanation:** When applying multiple conditions, use `&` for AND operations and `|` (pipe) for OR operations. **Crucial detail:** Each individual condition must be enclosed in parentheses `()` to prevent bitwise evaluation errors.[cite: 1]
**Example Code:**

```python

# Filter for non-churned males

filtered_df = df[(df['gender'] == 'Male') & (df['churn'] == 'No')]
```

---

### Counting Unique Values

**Explanation:** To prevent counting duplicated records (e.g., overlapping customer IDs), extract the target column and apply the `.nunique()` method to find the exact count of distinct values.[cite: 1]
**Example Code:**

```python
unique_customers = df['customerID'].nunique()
```

---

### Grouping and Aggregation

**Explanation:** Aggregation occurs in two steps: `.groupby()` groups identical values in a column, and `.agg()` applies math/summary functions to those groups. You can pass a dictionary mapping specific columns to functions (like `'mean'` or `'count'`). Alternatively, you can use a shortcut method by indexing a specific column after grouping. Null values are skipped by default.[cite: 1]
**Example Code:**

```python

# Method 1: Using agg with a dictionary

df.groupby('churn').agg({
'tenure': 'mean',
'customerID': 'count'
})

# Method 2: Shortcut by indexing the column

df.groupby('churn')['customerID'].count()
```

---

### Merging DataFrames (Joins)

**Explanation:** Similar to SQL, `pd.merge()` combines two DataFrames based on a common column. It takes parameters for the left table, right table, `on` (the shared key), and `how` (the join type: `'inner'`, `'left'`, `'right'`, etc.). If conflicting columns exist, Pandas automatically appends `_x` and `_y` suffixes. Merge handles exactly two tables at a time; multiple joins must be done sequentially.[cite: 1]
**Example Code:**

```python
df2 = pd.merge(df, cust_df, on='customerID', how='inner')
```

---

### Value Counts & Normalization

**Explanation:** The `.value_counts()` method groups by a specific column, counts the occurrences of each unique value, and automatically sorts them in descending order. By passing the parameter `normalize=True`, it converts absolute counts into relative percentages.[cite: 1]
**Example Code:**

```python

# Absolute frequency counts

df['Contract'].value_counts()

# Percentage of total (e.g., finding percentage of Veg food)

df['FoodType'].value_counts(normalize=True)
```

---

### Set Operations for Exclusion (Left Exclusive)

**Explanation:** When standard Pandas joins don't neatly solve an exclusion problem (e.g., finding users who _never_ placed an order), you can convert the identifier columns into standard Python `set()` structures and subtract one from the other to find elements unique to the first set.[cite: 1]
**Example Code:**

```python

# Find UserIDs present in the user table but missing from the orders table

users_without_orders = set(user_df['UserID']) - set(order_df['OrderID'])
count_missing = len(users_without_orders)
```
