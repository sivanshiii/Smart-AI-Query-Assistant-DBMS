# helpers.py

from db_connect import db   # import LangChain SQLDatabase connection

# Helper Function 1
def convert_output_to_string_list(output):
    """
    Converts a nested tuple structure into a list of strings.
    """
    def flatten_tuple(nested_tuple):
        for item in nested_tuple:
            if isinstance(item, tuple):
                yield from flatten_tuple(item)
            else:
                yield item
    return list(flatten_tuple(output))


# Helper Function 2
def sanitize_data(output) -> list[str]:
    """
    Sanitizes a string containing data within parentheses and delimiters.
    """
    final_output = []
    for i in output.split('),'):
        final_output.append(i)
    final_output = [
        i.replace('(', '')
         .replace(')', '')
         .replace("'", '')
         .replace(',', '')
         .replace('[', '')
         .replace(']', '')
        for i in final_output
    ]
    return final_output


# Helper Function 3
def get_metadata(schema: str, table_name: str) -> list[dict]:
    """ 
    Retrieves metadata for a table & its column info from PostgreSQL.
    """
    table_comments = db.run(
        f"SELECT description FROM pg_description WHERE objoid = 'public.{table_name}'::regclass"
    )
    col_comments = db.run(
        f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='{table_name}'"
    )

    final_tb_coments = sanitize_data(str(table_comments))
    final_col_coments = sanitize_data(str(col_comments))

    for i in range(len(final_col_coments)):
        final_col_coments[i] = f"{table_name}.{final_col_coments[i].strip()}"

    table_comm_d = {}
    table_comm_d[table_name] = (
        convert_output_to_string_list(final_tb_coments)[0]
        if final_tb_coments
        else "No comment"
    )

    col_comm_d = list(
        zip(final_col_coments, convert_output_to_string_list(final_tb_coments)[1:])
    )

    return [table_comm_d, col_comm_d, final_col_coments]
