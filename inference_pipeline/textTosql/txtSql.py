from langchain_openai import ChatOpenAI
import llm as templates
from llm import GeneralChain
from config import settings

import pandas as pd
import os
import duckdb
import sqlalchemy


class CSVDuckDBSink:
    path = settings._file_path

    def __init__(self):
        self.df = pd.read_csv(self.path)
        self.con = duckdb.connect(':memory:')  # Create an in-memory DuckDB database
        self.con.register('TikToktable', self.df)

    def generate_sql(query: str) -> str:
        texttosql_template = templates.TextToSqlTemplate()
        prompt_template = texttosql_template.create_template()

        model = ChatOpenAI(model=settings.OPENAI_MODEL_ID)
        chain = GeneralChain.get_chain(
            llm=model, output_key="text_sql", template=prompt_template
        )

        response = chain.invoke({"query": query})
        return response["text_sql"]

    def execute_sql_query(self, query) -> str:
        sqlQuery = self.generate_sql(query)
        return self.con.execute(sqlQuery) # need to check the result

csvRetriever = CSVDuckDBSink()


