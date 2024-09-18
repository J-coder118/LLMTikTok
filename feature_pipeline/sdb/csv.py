import pandas as pd
import os
import duckdb
import sqlalchemy

from  config import settings

class CSVSource:
    path = settings._file_path

    def __init__(self):
        self.df = pd.read_csv(path)  # Read the CSV file into a DataFrame
        self.index = 0  # Initialize an index to track the current row

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.df):
            row = self.df.iloc[self.index]  # Get the current row
            self.index += 1  # Move to the next row
            return row.to_dict()  # Return the row as a dictionary
        else:
            raise StopIteration  # Stop iteration when all rows are processed

csv_source = CSVSource()


class CSVDuckDBSink:
    path = settings._file_path

    def __init__(self):
        self.df = pd.read_csv(path)
        self.con = duckdb.connect(':memory:')  # Create an in-memory DuckDB database
        self.con.register('TikToktable', self.df)

    def execute_sql_query(self, query):
        return self.con.execute(query) # need to check the result

csv_table = CSVDuckDBSink()