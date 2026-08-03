import sqlite3
import os

def print_table_data(table_name):
    print(f"\n--- Data from '{table_name}' table ---")
    db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in cursor.fetchall()]
        print(" | ".join(columns))
        print("-" * 50)
        
        # Get rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(" | ".join(map(str, row)))
            
        conn.close()
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")

if __name__ == "__main__":
    print("Welcome to Fantasy Cricket Database Viewer!")
    print_table_data("stats")
    print_table_data("match")
    print_table_data("teams")
