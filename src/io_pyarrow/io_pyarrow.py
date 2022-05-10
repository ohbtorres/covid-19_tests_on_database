# Leitura de arquivos CSV com auxilio do pyarrow
from pyarrow import csv, Table, parquet

def pyarrow_read_csv(source,sep=","):
    return csv.read_csv(source,parse_options=csv.ParseOptions(delimiter=sep)).to_pandas()

def pyarrow_write_csv(dataframe_pandas,file_name):
    csv.write_csv(data = Table.from_pandas(dataframe_pandas),output_file = file_name)
    
def read_table_to_pandas(file_name):
    return parquet.read_table(file_name).to_pandas()

def write_table_from_pandas(dataframe_pandas,file_name):
    parquet.write_table(Table.from_pandas(dataframe_pandas),file_name)