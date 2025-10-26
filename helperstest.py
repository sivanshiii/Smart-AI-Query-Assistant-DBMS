# test_helpers.py
from helpers import get_metadata

# Example test
schema = "public"
table_name = "opportunities"  # 👈 replace with a table in your DB

result = get_metadata(schema, table_name)
print(result)
from db_connect import db
from helpers import get_metadata

print(db.get_table_info())  # built-in LangChain schema summary
print(get_metadata("public", "opportunities"))  # your custom version
