#2. Database Import Program - this database import programm efficiently transforms raw baseball data into a stuctured
# SQLite database,making it ready for analysis and visualization. It reads multiple CSV files, cleans and standardizes
#column names, and imports them into well labeled tables. The script includes checks for missing files, informative logging,
#and summarizes the tables created - ensuring transparancy and ease of debugging. This step forms the foundation of the 
#entire project,enabling clean, queryable access to historical MLB statistics and events.


import pandas as pd
import sqlite3
import os

#  CSV file paths and  table names
csv_table_map = {
    '../mlb_history/mlb_yearly_pages.csv': 'mlb_yearly_pages',
    '../mlb_history/mlb_events.csv': 'mlb_events',
    '../mlb_history/mlb_stats.csv': 'mlb_stats'
}

# SQLite database file name
db_filename = "mlb_history.db"

# connect to SQLite database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

for csv_file, table_name in csv_table_map.items():
    try:
        if not os.path.exists(csv_file):
            print(f" File not found: {csv_file}")
            continue

        print(f" Importing {csv_file} into table `{table_name}`...")

        # Read CSV into DataFrame
        df = pd.read_csv(csv_file)

        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Import into SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"Imported {len(df)} rows into `{table_name}`")

    except Exception as e:
        print(f" Error importing {csv_file}: {e}")

print("\n Tables in database:")
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
for t in tables:
    print(f" - {t[0]}")


conn.close()
print(f"\n Import complete. Database saved as: {db_filename}")

#preview first few rows
#SELECT * FROM mlb_yearly_pages LIMIT 5;
#SELECT * FROM mlb_events LIMIT 5;
#SELECT * FROM mlb_stats LIMIT 5;

#count rows per table
#SELECT COUNT(*) FROM mlb_yearly_pages;
#SELECT COUNT(*) FROM mlb_events;
#SELECT COUNT(*) FROM mlb_stats;
