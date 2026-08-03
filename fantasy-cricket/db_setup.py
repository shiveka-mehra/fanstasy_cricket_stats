import sqlite3
import os

def setup_database():
    db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match (
            Player TEXT,
            Scored INTEGER,
            Faced INTEGER,
            Fours INTEGER,
            Sixes INTEGER,
            Bowled INTEGER,
            Maiden INTEGER,
            Given INTEGER,
            Wkts INTEGER,
            Catches INTEGER,
            Stumping INTEGER,
            RO INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            player TEXT,
            matches INTEGER,
            runs INTEGER,
            "100s" INTEGER,
            "50s" INTEGER,
            value INTEGER,
            ctg TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT,
            players TEXT,
            value INTEGER
        )
    ''')

    # Clear existing data to avoid duplicates if run multiple times
    cursor.execute('DELETE FROM match')
    cursor.execute('DELETE FROM stats')
    
    # Data to insert
    data = [
        ("Kohli", 102, 98, 8, 2, 0, 0, 0, 0, 0, 0, 1, 120, 189, 8257, 28, 43, "BAT"),
        ("Yuvraj", 12, 20, 1, 0, 48, 0, 36, 1, 0, 0, 0, 100, 86, 3589, 10, 21, "BAT"),
        ("Rahane", 49, 75, 3, 0, 0, 0, 0, 0, 0, 0, 1, 100, 158, 5435, 11, 31, "BAT"),
        ("Dhawan", 32, 35, 4, 0, 0, 0, 0, 0, 0, 0, 0, 85, 25, 565, 2, 1, "AR"),
        ("Dhoni", 56, 45, 3, 1, 0, 0, 0, 0, 3, 2, 0, 75, 78, 2573, 3, 19, "WK"), # Note: Assuming Dhoni as WK because he is usually a WK, though PDF said BAT. Wait, PDF says BAT. I will use BAT as per PDF. Wait! Let me check the PDF exactly.
    ]

    # Re-evaluating data to match PDF exactly:
    pdf_data = [
        ("Kohli", 102, 98, 8, 2, 0, 0, 0, 0, 0, 0, 1, 189, 8257, 28, 43, 120, "BAT"),
        ("Yuvraj", 12, 20, 1, 0, 48, 0, 36, 1, 0, 0, 0, 86, 3589, 10, 21, 100, "BAT"),
        ("Rahane", 49, 75, 3, 0, 0, 0, 0, 0, 1, 0, 0, 158, 5435, 11, 31, 100, "BAT"),
        ("Dhawan", 32, 35, 4, 0, 0, 0, 0, 0, 0, 0, 0, 25, 565, 2, 1, 85, "AR"),
        ("Dhoni", 56, 45, 3, 1, 0, 0, 0, 0, 3, 2, 0, 78, 2573, 3, 19, 75, "BAT"),
        ("Axar", 8, 4, 2, 0, 48, 2, 35, 1, 0, 0, 0, 67, 208, 0, 0, 100, "BWL"),
        ("Pandya", 42, 36, 3, 3, 30, 0, 25, 0, 1, 0, 0, 70, 77, 0, 0, 75, "BWL"),
        ("Jadeja", 18, 10, 1, 1, 60, 3, 50, 2, 1, 0, 1, 16, 1, 0, 0, 85, "BWL"),
        ("Kedar", 65, 60, 7, 0, 24, 0, 24, 0, 0, 0, 0, 111, 675, 0, 1, 90, "BWL"),
        ("Ashwin", 23, 42, 3, 0, 60, 2, 45, 6, 0, 0, 0, 136, 1914, 0, 10, 100, "AR"),
        ("Umesh", 0, 0, 0, 0, 54, 0, 50, 4, 1, 0, 0, 296, 9496, 10, 64, 110, "WK"),
        ("Bumrah", 0, 0, 0, 0, 60, 2, 49, 1, 0, 0, 0, 73, 1365, 0, 8, 60, "WK"),
        ("Bhuvaneshwar", 15, 12, 2, 0, 60, 1, 46, 2, 0, 0, 0, 17, 289, 0, 2, 75, "AR"),
        ("Rohit", 46, 65, 5, 1, 0, 0, 0, 0, 1, 0, 0, 304, 8701, 14, 52, 85, "BAT"),
        ("Kartick", 29, 42, 3, 0, 0, 0, 0, 0, 2, 0, 1, 11, 111, 0, 0, 75, "AR")
    ]

    for row in pdf_data:
        # Match table data: player, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro
        match_record = row[:12]
        
        # Stats table data: player, matches, runs, 100s, 50s, value, ctg
        stats_record = (row[0], row[12], row[13], row[14], row[15], row[16], row[17])
        
        cursor.execute('''
            INSERT INTO match (Player, Scored, Faced, Fours, Sixes, Bowled, Maiden, Given, Wkts, Catches, Stumping, RO)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', match_record)
        
        # NOTE: Using the column name "100s" and "50s" in SQLite query requires quotes
        cursor.execute('''
            INSERT INTO stats (player, matches, runs, "100s", "50s", value, ctg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', stats_record)

    conn.commit()
    conn.close()
    print("Database created and initialized successfully.")

if __name__ == '__main__':
    setup_database()
