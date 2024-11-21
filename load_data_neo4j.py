from neo4j import GraphDatabase
import psycopg2
from dotenv import load_dotenv
import os
# Neo4j Cloud Credentials
neo4j_uri = os.getenv('neo4j_uri')
neo4j_user = os.getenv('neo4j_user')
neo4j_password = os.getenv('neo4j_password')

def get_postgres_data():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="127.0.0.1"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players_scd")
    
    columns = ['player_name', 'scoring_class', 'is_active', 
               'start_season', 'end_season', 'current_season']
    
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    cursor.close()
    conn.close()
    return results

def load_to_neo4j(data):
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        driver.verify_connectivity()
        print("Connected to Neo4j Cloud!")

        # Updated constraint syntax
        driver.execute_query(
            "CREATE CONSTRAINT player_name IF NOT EXISTS FOR (p:Player) REQUIRE p.player_name IS UNIQUE",
            database_="neo4j"
        )

        # Load data
        for player in data:
            summary = driver.execute_query(
                """
                MERGE (p:Player {player_name: $player_name})
                CREATE (s:PlayerState {
                    scoring_class: $scoring_class,
                    is_active: $is_active,
                    start_season: $start_season,
                    end_season: $end_season,
                    current_season: $current_season
                })
                CREATE (p)-[:HAS_STATE]->(s)
                """,
                player,
                database_="neo4j"
            ).summary
            print(f"Created nodes for {player['player_name']}")

def query_data():
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        # Query all players and their states
        records, summary, keys = driver.execute_query(
            """
            MATCH (p:Player)-[:HAS_STATE]->(s:PlayerState)
            RETURN p.player_name as player, 
                   s.scoring_class as class,
                   s.start_season as season
            ORDER BY p.player_name, s.start_season
            """,
            database_="neo4j"
        )

        print("\nPlayer Data in Neo4j:")
        print("----------------------")
        for record in records:
            print(f"Player: {record['player']}, Class: {record['class']}, Season: {record['season']}")

        # Get statistics
        stats_records, _, _ = driver.execute_query(
            """
            MATCH (p:Player)
            RETURN count(p) as player_count
            """,
            database_="neo4j"
        )
        
        print(f"\nTotal Players: {stats_records[0]['player_count']}")

if __name__ == "__main__":
    # Get data from PostgreSQL
    players_data = get_postgres_data()
    
    # Load to Neo4j
    load_to_neo4j(players_data)
    
    # Query and display results
    query_data()
