# query_execution.py

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from query_cleaner import clean_sql_quer
from helpers import get_metadata
from db_connect import db  # your existing connection
import re

# --- Initialize LLM ---
llm = OllamaLLM(model="llama3")

# --- Use existing database object ---
print("✅ Database object loaded successfully!")

# --- Get metadata for clarity ---
table_info = db.get_table_info()
table_metadata = get_metadata("public", "opportunities")

# --- Prompt to guide LLM ---
sql_prompt = ChatPromptTemplate.from_template("""
You are an expert SQL assistant.
Given the schema below and a question, generate a syntactically correct SQL query 
that can be executed directly on PostgreSQL.

Schema:
{schema}

Question:
{question}

Return only the SQL query, nothing else.
""")

# --- User question ---
inp_query = input("Enter your question about the data: ")

# --- Generate SQL query ---
prompt_text = sql_prompt.format(schema=table_info, question=inp_query)
generated_sql = llm.invoke(prompt_text)

# --- Clean query ---
sql_query = clean_sql_quer(generated_sql.content if hasattr(generated_sql, "content") else str(generated_sql))
print("\n Cleaned SQL Query:\n", sql_query)

# --- Execute query safely ---
try:
    result = db.run(sql_query)
    print("\n Query Results:\n", result)
except Exception as e:
    print("\n Error while executing query:", e)

# --- Optional rephrased summary ---
rephrase_prompt = ChatPromptTemplate.from_template("""
You are a data assistant. 
Given a SQL query and its results, summarize the key information for a human in 2-3 sentences.

Query: {query}
Results: {results}
""")

summary = llm.invoke(rephrase_prompt.format(query=sql_query, results=str(result)))
print("\n Summary:\n", summary.content if hasattr(summary, "content") else summary)
