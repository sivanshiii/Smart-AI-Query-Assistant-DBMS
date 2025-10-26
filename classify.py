# ---------------------------------------------------
# Local Table Classifier using Ollama + Llama3
# ---------------------------------------------------

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

# ---------------------------------------------------
# Mock Metadata — replace with your actual ones
# ---------------------------------------------------
table_metadata = [
    {"accounts": "Contains account info like name, id, and contact details"},
    {"opportunities": "Contains sales opportunities and their stages"},
    {"contacts": "Contains individual contact information linked to accounts"},
]

col_metadata = [
    ("opportunities.account_id", "Links each opportunity to an account"),
    ("opportunities.stage", "Stage of the sales opportunity"),
    ("accounts.id", "Unique identifier for an account"),
]

# ---------------------------------------------------
# Prompt template for table classification
# ---------------------------------------------------
tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'TableClassification' function.

You have access to {table_metadata}. This is a list of dictionaries where each key is the table name and the value is the table description.
In addition, you have access to {col_metadata}. This is a list of tuples in (column, column description) format.

You must pick the table that directly contains the data required to answer the query,
not the one that only references it. For example, if the question asks about 
opportunity stages or counts by account_id, the correct table is likely "opportunities" 
(since that’s where stage and account_id are stored).

You should only have 1 answer after classification.

Passage:
{input}
"""
)


# ---------------------------------------------------
# Define structured output schema
# ---------------------------------------------------
class TableClassification(BaseModel):
    table_to_use: str = Field(description="The correct table to use for this query!")

# ---------------------------------------------------
# Load Ollama local model
# ---------------------------------------------------
llm_classification = ChatOllama(
    model="llama3",
    temperature=0
).with_structured_output(TableClassification)

# ---------------------------------------------------
# Test input query
# ---------------------------------------------------
inp_query = "which account id has the most number of opportunities in proposal stage?"

# ---------------------------------------------------
# Run the LLM classification
# ---------------------------------------------------
prompt = tagging_prompt.invoke({
    "input": inp_query,
    "table_metadata": table_metadata,
    "col_metadata": col_metadata
})

response = llm_classification.invoke(prompt)
table_info = response.dict()['table_to_use']

print("✅ The table that was identified for this query was:", table_info)
