# query_generation.py
from query_cleaner import clean_sql_quer
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM  

def execute_query(query: str):
    import psycopg2
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="varsha"  
    )
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# Use Ollama (local model)
generate_query = OllamaLLM(model="llama3", temperature=0)

# to test connection working or not, enter anything in the print stmt hehe
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3")
print(llm.invoke("is ollama working??"))
