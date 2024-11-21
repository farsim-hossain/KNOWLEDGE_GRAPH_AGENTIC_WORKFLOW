// get the players whos scoring_class is bad and end season is 2000


MATCH (p:Player)-[:HAS_STATE]->(s:PlayerState)
WHERE s.scoring_class = 'bad' 
AND s.end_season = 2000
RETURN p, s

// seeing all the nodes of each player

MATCH (p:Player)-[r:HAS_STATE]->(s:PlayerState)
WITH p, s
CREATE (sc:ScoringClass {value: s.scoring_class})
CREATE (ss:Season {value: 'Start: ' + toString(s.start_season)})
CREATE (es:Season {value: 'End: ' + toString(s.end_season)})
CREATE (cs:Season {value: 'Current: ' + toString(s.current_season)})
CREATE (act:Status {value: CASE s.is_active WHEN true THEN 'Active' ELSE 'Inactive' END})
CREATE (p)-[:HAS_PERFORMANCE]->(sc)
CREATE (p)-[:STARTED_IN]->(ss)
CREATE (p)-[:ENDED_IN]->(es)
CREATE (p)-[:CURRENT_IN]->(cs)
CREATE (p)-[:STATUS]->(act)
RETURN *
