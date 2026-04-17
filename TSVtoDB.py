<<<<<<< HEAD
import pandas as pd
import sqlite3

TSV_FILE = r"D:\Projects\Test-InApp\datasets\title.basics.tsv"
DB_FILE = r"D:\Projects\Test-InApp\Database\MovieInfo.db"
TABLE_NAME = "title_basics"

conn = sqlite3.connect(DB_FILE)


conn.execute("PRAGMA journal_mode = WAL;")
conn.execute("PRAGMA synchronous = NORMAL;")

chunk_size = 500  # Adjust based on memory


for i, chunk in enumerate(pd.read_csv(
        TSV_FILE,
        sep="\t",
        dtype=str,
        chunksize=500,  # reduce to stay under SQLite limit
        encoding="utf-8",
        na_values=["", "NULL", "\\N"],
        keep_default_na=False
)):
    chunk = chunk.replace("\\N", pd.NA)
    chunk.to_sql(
        TABLE_NAME,
        conn,
        if_exists="append",
        index=False,
        method=None  # avoid multi-row batching
    )


conn.close()

=======
import pandas as pd
import sqlite3

TSV_FILE = r"D:\Projects\Test-InApp\datasets\title.basics.tsv"
DB_FILE = r"D:\Projects\Test-InApp\Database\MovieInfo.db"
TABLE_NAME = "title_basics"

conn = sqlite3.connect(DB_FILE)


conn.execute("PRAGMA journal_mode = WAL;")
conn.execute("PRAGMA synchronous = NORMAL;")

chunk_size = 500  # Adjust based on memory


for i, chunk in enumerate(pd.read_csv(
        TSV_FILE,
        sep="\t",
        dtype=str,
        chunksize=500,  # reduce to stay under SQLite limit
        encoding="utf-8",
        na_values=["", "NULL", "\\N"],
        keep_default_na=False
)):
    chunk = chunk.replace("\\N", pd.NA)
    chunk.to_sql(
        TABLE_NAME,
        conn,
        if_exists="append",
        index=False,
        method=None  # avoid multi-row batching
    )


conn.close()

>>>>>>> bc2e5fc12afadfe2875471f499d61556b576b3b7
print("TSV successfully loaded into SQLite!")