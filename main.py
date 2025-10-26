from query_cleaner import clean_sql_quer

# Example: test the cleaner
raw_sql = """```sql
SQLQuery:
SELECT * FROM `oppurtunities` WHERE id = 1;```"""

cleaned_sql = clean_sql_quer(raw_sql)
print("Cleaned SQL:\n", cleaned_sql)


