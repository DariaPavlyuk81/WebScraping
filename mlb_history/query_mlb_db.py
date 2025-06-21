#3. Database Query Program

#This CLI(commandline interface) programme provides a simple yet powerful way to explore the MLB dtabase using custom
#SQL queries. It connects to the SQlite database,users can find some example queries. Results are displayed in a clean
#format, making it easy to eneterplet player stats, seasonal data and historical events. There is a built-in-error handling,


#DB_FILE = "mlb_history.db" Tells the script what file to connect to
#connect_db() opens the database, without this there is no data to query
#run_query() takes a user's SQL input, runs it, and shows results in a readable table. It is like a translator 
#from human command to database to readable output
#show_intro() friendly warning how to use the tool
#main() event loop - it runs everything:connects to DB, shows the intro, then keeps asking for queries until you exit


#SELECT player, category, value, year
#FROM mlb_stats
#WHERE category = 'Batting Average'
#ORDER BY year DESC
#LIMIT 10;



#SELECT s.year, s.player, s.category, s.value, e.world_series
#FROM mlb_stats s
#JOIN mlb_events e ON s.year = e.year
#WHERE s.category = 'ERA'
#ORDER BY s.year;







import sqlite3
import os

DB_FILE = "mlb_history.db"

def show_intro():
    print("\n MLB History Query CLI")
    print("Type SQL queries to explore the data.")
    print("Examples:")
    print("  SELECT * FROM mlb_stats WHERE year = 1998 AND category = 'Home Runs';")
    print("  SELECT s.year, s.player, s.value, e.world_series FROM mlb_stats s JOIN mlb_events e ON s.year = e.year WHERE s.category = 'ERA';")
    print("Type '.exit' to quit.\n")

def connect_db():
    if not os.path.exists(DB_FILE):
        print(f" Database file '{DB_FILE}' not found.")
        return None
    return sqlite3.connect(DB_FILE)

def run_query(cursor, query):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        # Print results as a table
        print(f"\n {len(rows)} rows returned.")
        print("-" * 60)
        print(" | ".join(columns))
        print("-" * 60)
        for row in rows:
            print(" | ".join(str(cell) for cell in row))
        print()
    except Exception as e:
        print(f"⚠️ Query error: {e}")

def main():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    show_intro()

    while True:
        user_input = input("sql> ").strip()
        if user_input.lower() in ['exit', '.exit', 'quit']:
            print(" Goodbye!")
            break
        elif user_input:
            run_query(cursor, user_input)

    conn.close()

if __name__ == "__main__":
    main()
