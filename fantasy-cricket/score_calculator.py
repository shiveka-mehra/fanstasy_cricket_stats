def calculate_points(row):
    """
    row: dictionary or tuple containing match stats for a player.
    Indices based on database match table:
    (Player, Scored, Faced, Fours, Sixes, Bowled, Maiden, Given, Wkts, Catches, Stumping, RO)
    """
    # Assuming row is a dictionary for easier access, if it's a tuple, we'll map it
    if isinstance(row, tuple):
        stats = {
            'runs': row[1],
            'faced': row[2],
            'fours': row[3],
            'sixes': row[4],
            'bowled': row[5],
            'maiden': row[6],
            'given': row[7],
            'wkts': row[8],
            'catches': row[9],
            'stumping': row[10],
            'ro': row[11]
        }
    else:
        stats = row

    points = 0.0

    # BATTING
    runs = stats['runs']
    faced = stats['faced']
    fours = stats['fours']
    sixes = stats['sixes']

    # 1 point for 2 runs scored
    points += runs / 2.0

    # Additional 5 points for half century
    if runs >= 50 and runs < 100:
        points += 5
    # Additional 10 points for century
    if runs >= 100:
        points += 10 # Assuming century points replace half century points, or maybe it's 5 + 10. Let's assume 10.

    # Strike rate points
    if faced > 0:
        strike_rate = (runs / faced) * 100
        if 80 <= strike_rate <= 100:
            points += 2
        elif strike_rate > 100:
            points += 4 # Additional 4 points for strike rate > 100 (some interpretations use 6 total, we'll use 4)

    # Boundaries
    points += fours * 1
    points += sixes * 2

    # BOWLING
    bowled = stats['bowled']
    given = stats['given']
    wkts = stats['wkts']

    # 10 points for each wicket
    points += wkts * 10

    # Additional points for wickets
    if wkts >= 3 and wkts < 5:
        points += 5
    if wkts >= 5:
        points += 10

    # Economy rate points
    if bowled > 0:
        overs = bowled / 6.0
        eco_rate = given / overs
        if 3.5 <= eco_rate <= 4.5:
            points += 4
        elif 2 <= eco_rate < 3.5:
            points += 7
        elif eco_rate < 2:
            points += 10

    # FIELDING
    catches = stats['catches']
    stumping = stats['stumping']
    ro = stats['ro']

    points += (catches + stumping + ro) * 10

    return points
