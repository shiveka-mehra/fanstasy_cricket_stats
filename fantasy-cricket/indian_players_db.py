import sqlite3
import os
import random

def get_indian_players():
    # Names, Category, Value
    players = [
        # BATSMEN
        ("Virat Kohli", "BAT", 120),
        ("Rohit Sharma", "BAT", 115),
        ("Shikhar Dhawan", "BAT", 100),
        ("Ajinkya Rahane", "BAT", 95),
        ("Cheteshwar Pujara", "BAT", 90),
        ("KL Rahul", "BAT", 105),
        ("Shreyas Iyer", "BAT", 95),
        ("Suryakumar Yadav", "BAT", 110),
        ("Shubman Gill", "BAT", 100),
        ("Yashasvi Jaiswal", "BAT", 90),
        ("Ruturaj Gaikwad", "BAT", 85),
        ("Mayank Agarwal", "BAT", 80),
        ("Karun Nair", "BAT", 75),
        ("Manish Pandey", "BAT", 80),
        ("Ambati Rayudu", "BAT", 85),
        ("Rinku Singh", "BAT", 90),
        ("Tilak Varma", "BAT", 80),
        
        # WICKET KEEPERS
        ("MS Dhoni", "WK", 110),
        ("Rishabh Pant", "WK", 105),
        ("Sanju Samson", "WK", 95),
        ("Ishan Kishan", "WK", 95),
        ("Wriddhiman Saha", "WK", 85),
        ("Dinesh Karthik", "WK", 90),
        ("KS Bharat", "WK", 75),
        ("Jitesh Sharma", "WK", 80),
        ("Dhruv Jurel", "WK", 85),
        ("Parthiv Patel", "WK", 80),
        
        # ALL ROUNDERS
        ("Hardik Pandya", "AR", 115),
        ("Ravindra Jadeja", "AR", 110),
        ("Ravichandran Ashwin", "AR", 105),
        ("Axar Patel", "AR", 100),
        ("Washington Sundar", "AR", 85),
        ("Shivam Dube", "AR", 90),
        ("Krunal Pandya", "AR", 85),
        ("Deepak Hooda", "AR", 80),
        ("Shardul Thakur", "AR", 90),
        ("Stuart Binny", "AR", 70),
        ("Vijay Shankar", "AR", 75),
        
        # BOWLERS
        ("Jasprit Bumrah", "BOW", 120),
        ("Mohammed Shami", "BOW", 110),
        ("Bhuvneshwar Kumar", "BOW", 105),
        ("Umesh Yadav", "BOW", 90),
        ("Ishant Sharma", "BOW", 95),
        ("Mohammed Siraj", "BOW", 105),
        ("Yuzvendra Chahal", "BOW", 100),
        ("Kuldeep Yadav", "BOW", 100),
        ("Amit Mishra", "BOW", 85),
        ("Arshdeep Singh", "BOW", 95),
        ("Mukesh Kumar", "BOW", 80),
        ("Avesh Khan", "BOW", 85),
        ("Prasidh Krishna", "BOW", 85),
        ("Navdeep Saini", "BOW", 80),
        ("Deepak Chahar", "BOW", 90),
        ("Rahul Chahar", "BOW", 80),
        ("Ravi Bishnoi", "BOW", 90),
        ("T Natarajan", "BOW", 85),
        ("Sandeep Sharma", "BOW", 85),
        ("Mohit Sharma", "BOW", 85),
        ("Harshal Patel", "BOW", 90),
        ("Khaleel Ahmed", "BOW", 80)
    ]
    
    records = []
    for p in players:
        name, ctg, val = p
        
        # generate random reasonable stats based on category
        matches = random.randint(20, 150)
        
        if ctg == "BAT":
            runs = random.randint(1000, 6000)
            hundreds = random.randint(0, 15)
            fifties = random.randint(5, 30)
            scored = random.randint(20, 120)
            faced = scored + random.randint(-10, 20)
            fours = random.randint(2, 10)
            sixes = random.randint(0, 5)
            bowled, maiden, given, wkts = 0, 0, 0, 0
            catches, stumping, ro = random.randint(0,2), 0, random.randint(0,1)
        elif ctg == "WK":
            runs = random.randint(1000, 4000)
            hundreds = random.randint(0, 5)
            fifties = random.randint(5, 20)
            scored = random.randint(10, 80)
            faced = scored + random.randint(-10, 20)
            fours = random.randint(1, 8)
            sixes = random.randint(0, 4)
            bowled, maiden, given, wkts = 0, 0, 0, 0
            catches, stumping, ro = random.randint(1,4), random.randint(0,2), random.randint(0,1)
        elif ctg == "AR":
            runs = random.randint(500, 3000)
            hundreds = random.randint(0, 2)
            fifties = random.randint(2, 15)
            scored = random.randint(10, 60)
            faced = scored + random.randint(-5, 10)
            fours = random.randint(1, 6)
            sixes = random.randint(0, 3)
            bowled = random.randint(12, 60)
            maiden = random.randint(0, 2)
            given = random.randint(15, 60)
            wkts = random.randint(0, 3)
            catches, stumping, ro = random.randint(0,1), 0, random.randint(0,1)
        else: # BOW
            runs = random.randint(50, 500)
            hundreds = 0
            fifties = random.randint(0, 1)
            scored = random.randint(0, 20)
            faced = scored + random.randint(0, 10)
            fours = random.randint(0, 2)
            sixes = random.randint(0, 1)
            bowled = random.randint(24, 60)
            maiden = random.randint(0, 3)
            given = random.randint(15, 60)
            wkts = random.randint(1, 5)
            catches, stumping, ro = random.randint(0,1), 0, 0
            
        match_record = (name, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro)
        stats_record = (name, matches, runs, hundreds, fifties, val, ctg)
        
        records.append((match_record, stats_record))
        
    return records

def reset_and_populate_db():
    db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Wipe the existing players
    cursor.execute('DELETE FROM match')
    cursor.execute('DELETE FROM stats')
    # Also wipe teams since the old teams will have invalid players
    cursor.execute('DELETE FROM teams')
    
    records = get_indian_players()
    count = 0
    for match_record, stats_record in records:
        cursor.execute('''
            INSERT INTO match (Player, Scored, Faced, Fours, Sixes, Bowled, Maiden, Given, Wkts, Catches, Stumping, RO)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', match_record)
        
        cursor.execute('''
            INSERT INTO stats (player, matches, runs, "100s", "50s", value, ctg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', stats_record)
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Database reset and populated with {count} Indian players successfully.")

if __name__ == '__main__':
    reset_and_populate_db()
