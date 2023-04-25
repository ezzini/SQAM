# Structural Query Alignment Metric (SQAM)

The Structural Query Alignment Metric (SQAM) is a Python package that provides functions to compare SQL queries based on their syntax and structure. Given a query and a ground truth query, the package computes an accuracy score that reflects the degree of similarity between the two queries. The accuracy score is based on the percentage of matching query subitems (e.g., select columns, where conditions, order by clauses) weighted by their importance in the overall query structure.

## Installation

To install the SQL Query Comparator package, run the following command:

```
git clone https://github.com/ezzini/SQAM.git
```

## Usage

### Batch evaluation

To use the SQAM metric for batch evaluation, import the `sql_query_accuracy()` function from the `sqam` module:

```python
from SQAM.sqam import sqam_batch
```

The `sqam_batch()` function takes two arguments: a list of queries to evaluate, and a list of ground truth queries for comparison. The lists should have the same length. The function returns an accuracy score between 0 and 100.

Here's an example of how to use the `sqam_batch()` function:

```python
test_queries = ["SELECT name, age FROM users WHERE age >= 18 ORDER BY name ASC",
  "SELECT col1, col2, col3, col0 FROM table1 JOIN table2 ON table1.id = table2.id WHERE col1 > 10 LIMIT 2"]
true_queries = ["SELECT name, age FROM users WHERE age > 17 ORDER BY name ASC",
  "SELECT col1, col4, col0, col2 FROM table2 JOIN table3 ON table1.id = table2.id WHERE col1 = 10 LIMIT 2"]

accuracy = sqam_batch(test_queries, true_queries)

print(f"Accuracy score: {accuracy:.2f}%")
```

### Unit evaluation

For unit evaluation, import the `sql_query_accuracy()` function from the `sqam` module:

```python
from SQAM.sqam import sql_query_accuracy
```

The `sql_query_accuracy()` function takes two arguments: a query to evaluate, and a ground truth query for comparison. The function returns an accuracy score between 0 and 100.

Here's an example of how to use the `sql_query_accuracy()` function:

```python
query = "SELECT name, age FROM users WHERE age >= 18 ORDER BY name ASC"
true_query = "SELECT name, age FROM users WHERE age > 17 ORDER BY name ASC"

accuracy = sql_query_accuracy(query, true_query)

print(f"Accuracy score: {accuracy:.2f}%")
```

This code will output:

```
Accuracy score: 75.00%
```

## How it works

The `sql_query_accuracy()` function works by splitting the input queries into their main parts (e.g., SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY) using regular expressions. Each part is then further split into its subitems (e.g., select columns, table names, where conditions) using additional regular expressions.

The function then computes an accuracy score by comparing the subitems in the input query with those in the ground truth query. The subitems are weighted by their importance in the query structure (e.g., the SELECT clause is weighted more heavily than the ORDER BY clause), and the accuracy score is calculated as the percentage of matching subitems weighted by their importance.

## Limitations

The SQL Query Comparator package has several limitations:

- The package only compares queries based on their syntax and structure, not their semantics. In other words, the package cannot determine whether two queries produce the same result set, only whether they have similar syntax and structure.
- The regular expressions used to split the queries into parts and subitems may not work correctly for all queries. In particular, complex or nested queries may not be split correctly.
- The weighting scheme used to weight the query parts may not be appropriate for all use cases. Users may need to modify the weighting scheme to reflect their specific needs.

## Contributing

Contributions to the SQL Query Comparator package are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request on the GitHub repository.

## License

The SQAM package is released under the MIT license. See the LICENSE file for more information.
