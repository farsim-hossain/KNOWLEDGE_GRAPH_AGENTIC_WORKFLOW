// Get all states for a specific player
MATCH (p:Player {player_name: 'player_name'})-[:HAS_STATE]->(s:PlayerState)
RETURN p, s
ORDER BY s.start_season;

// Find all 'star' players in current season
MATCH (p:Player)-[:HAS_STATE]->(s:PlayerState)
WHERE s.scoring_class = 'star' 
AND s.end_season = 9999
RETURN p, s;

// Track scoring progression
MATCH (p:Player)-[:HAS_STATE]->(s:PlayerState)
RETURN p.player_name, 
       collect(s.scoring_class) as progression,
       collect(s.start_season) as seasons
ORDER BY p.player_name;
