import pandas as pd
import os
import duckdb
import logging

from  config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVSource:
    path = settings._file_path

    def __init__(self):
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                self.df = pd.read_csv(self.path, encoding=encoding)  # Specify the encoding
                self.index = 0  # Initialize an index to track the current row
                logger.info(f"Successfully loaded CSV file from {self.path}")
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to read CSV file with encoding {encoding}, trying next encoding.")
            except FileNotFoundError:
                logger.error(f"File not found: {self.path}")
                raise
            except pd.errors.EmptyDataError:
                logger.error(f"Empty data: {self.path}")
                raise
            except Exception as e:
                logger.error(f"Error reading CSV file: {e}")
                raise
        else:
            raise ValueError(f"Failed to read CSV file with all attempted encodings.")

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
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                self.df = pd.read_csv(self.path, encoding=encoding)  # Specify the encoding
                self.con = duckdb.connect(':memory:')  # Create an in-memory DuckDB database
                self.con.register('TikToktable', self.df)
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to read CSV file with encoding {encoding}, trying next encoding.")
            except FileNotFoundError:
                logger.error(f"File not found: {self.path}")
                raise
            except pd.errors.EmptyDataError:
                logger.error(f"Empty data: {self.path}")
                raise
            except Exception as e:
                logger.error(f"Error reading CSV file: {e}")
                raise
        else:
            raise ValueError(f"Failed to read CSV file with all attempted encodings.")
        

    def execute_sql_query(self, query):
        return self.con.execute(query) # need to check the result

csv_table = CSVDuckDBSink()