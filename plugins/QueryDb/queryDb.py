from typing import Annotated,Optional #,List, Optional, TypedDict
from semantic_kernel.functions import kernel_function #, kernel_function_context_parameter
#from semantic_kernel import KernelContext

import pyodbc


class QueryDbPlugin:
    """
    Description: Get the result of a SQL query
    """
    def __init__(self, connection_string) -> None:
        self._connection_string = connection_string
    
    @staticmethod
    def __clean_sql_query__(sql_query):
        sql_query = sql_query.replace(";", "")
        sql_query = sql_query.replace("/n ", " ")
        sql_query = sql_query.replace("T-SQL:", "")
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")

        return sql_query  
    
    @kernel_function(name="query_db",
                     description="SQLクエリを使用してデータベースに問い合わせる")
    def query_db(self, input: Annotated[str, "実行するSQLクエリ"]) -> Annotated[Optional[list], "結果を得るためにデータベースに問い合わせる。"]:   
        # Connect to the SQL Server database
        conn = pyodbc.connect(self._connection_string)
        print(f"input=☆{self.__clean_sql_query__(input)}☆")
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        print(f"★★★★★★★★★★★★★★★★★★★★★★★★")
        try:
            sql = self.__clean_sql_query__(input)
            print(f"sql={sql}")
            cursor.execute(sql)
            #result = cursor.fetchone()
            
            # Get the column names from cursor.description
            columns = [column[0] for column in cursor.description]

            # Initialize an empty list to store the results as dictionaries
            results = []

            # Fetch all rows and create dictionaries
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            return f"Error: {e}"
        cursor.close()
        conn.close()
        
        return str(results)
