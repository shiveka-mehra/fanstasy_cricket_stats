import sqlite3
import os
import random

def get_more_players():
    # Names, Category, Value
    players = [
        # BAT
        ("Sachin Tendulkar", "BAT", 120),
        ("Virender Sehwag", "BAT", 110),
        ("Gautam Gambhir", "BAT", 100),
        ("Suresh Raina", "BAT", 95),
        ("Shubman Gill", "BAT", 95),
        ("Suryakumar Yadav", "BAT", 100),
        ("Shreyas Iyer", "BAT", 90),
        ("KL Rahul", "BAT", 95),
        ("David Warner", "BAT", 110),
        ("Steve Smith", "BAT", 115),
        ("Kane Williamson", "BAT", 115),
        ("Joe Root", "BAT", 115),
        ("Babar Azam", "BAT", 110),
        ("Quinton de Kock", "WK", 100), # WK
        ("Jos Buttler", "WK", 105), # WK
        ("Rishabh Pant", "WK", 95), # WK
        ("Sanju Samson", "WK", 90), # WK
        ("Ishan Kishan", "WK", 85), # WK
        ("Jonny Bairstow", "WK", 95), # WK
        ("Heinrich Klaasen", "WK", 90), # WK
        # AR
        ("Ben Stokes", "AR", 120),
        ("Hardik Pandya", "AR", 110), # duplicate, we will handle UNIQUE or just let it be duplicate if db allows, wait, we should check existing
        ("Ravindra Jadeja", "AR", 105), # duplicate
        ("Glenn Maxwell", "AR", 100),
        ("Shakib Al Hasan", "AR", 110),
        ("Marcus Stoinis", "AR", 90),
        ("Cameron Green", "AR", 85),
        ("Sam Curran", "AR", 95),
        ("Jason Holder", "AR", 90),
        ("Andre Russell", "AR", 105),
        # BOW
        ("Jasprit Bumrah", "BOW", 120), # duplicate
        ("Mohammed Shami", "BOW", 105),
        ("Mohammed Siraj", "BOW", 95),
        ("Rashid Khan", "BOW", 115),
        ("Trent Boult", "BOW", 105),
        ("Mitchell Starc", "BOW", 110),
        ("Pat Cummins", "BOW", 105),
        ("Kagiso Rabada", "BOW", 100),
        ("Shaheen Afridi", "BOW", 100),
        ("Jofra Archer", "BOW", 95),
        ("Yuzvendra Chahal", "BOW", 95),
        ("Kuldeep Yadav", "BOW", 90),
        ("Sunil Narine", "BOW", 100),
        ("Muttiah Muralitharan", "BOW", 110),
        ("Shane Warne", "BOW", 110),
        ("Glenn McGrath", "BOW", 110),
        ("Wasim Akram", "BOW", 110),
        ("Waqar Younis", "BOW", 105),
        ("Shoaib Akhtar", "BOW", 105),
        ("Brett Lee", "BOW", 105),
    ]
    
    records = []
    for p in players:
        name, ctg, val = p
        
        # generate random reasonable stats
        matches = random.randint(20, 200)
        
        if ctg == "BAT":
            runs = random.randint(1000, 10000)
            hundreds = random.randint(0, 30)
            fifties = random.randint(5, 50)
            scored = random.randint(20, 120)
            faced = scored + random.randint(-10, 20)
            fours = random.randint(2, 10)
            sixes = random.randint(0, 5)
            bowled, maiden, given, wkts = 0, 0, 0, 0
            catches, stumping, ro = random.randint(0,2), 0, random.randint(0,1)
        elif ctg == "WK":
            runs = random.randint(1000, 8000)
            hundreds = random.randint(0, 20)
            fifties = random.randint(5, 40)
            scored = random.randint(10, 80)
            faced = scored + random.randint(-10, 20)
            fours = random.randint(1, 8)
            sixes = random.randint(0, 4)
            bowled, maiden, given, wkts = 0, 0, 0, 0
            catches, stumping, ro = random.randint(1,4), random.randint(0,2), random.randint(0,1)
        elif ctg == "AR":
            runs = random.randint(500, 5000)
            hundreds = random.randint(0, 5)
            fifties = random.randint(2, 25)
            scored = random.randint(10, 60)
            faced = scored + random.randint(-5, 10)
            fours = random.randint(1, 6)
            sixes = random.randint(0, 3)
            bowled = random.randint(12, 60)
            maiden = random.randint(0, 2)
            given = random.randint(10, 60)
            wkts = random.randint(0, 3)
            catches, stumping, ro = random.randint(0,1), 0, random.randint(0,1)
        else: # BOW
            runs = random.randint(50, 1000)
            hundreds = 0
            fifties = random.randint(0, 2)
            scored = random.randint(0, 20)
            faced = scored + random.randint(0, 10)
            fours = random.randint(0, 2)
            sixes = random.randint(0, 1)
            bowled = random.randint(24, 60)
            maiden = random.randint(0, 3)
            given = random.randint(15, 60)
            wkts = random.randint(1, 5)
            catches, stumping, ro = random.randint(0,1), 0, 0
            
        # Match table data: player, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro
        match_record = (name, scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, ro)
        # Stats table data: player, matches, runs, 100s, 50s, value, ctg
        stats_record = (name, matches, runs, hundreds, fifties, val, ctg)
        
        records.append((match_record, stats_record))
        
    return records

def add_players():
    db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # get existing to avoid exact name duplicates
    cursor.execute("SELECT player FROM stats")
    existing_players = set([row[0] for row in cursor.fetchall()])
    
    records = get_more_players()
    count = 0
    for match_record, stats_record in records:
        name = stats_record[0]
        if name in existing_players:
            continue
            
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
    print(f"Added {count} new players successfully.")

if __name__ == '__main__':
    add_players()
