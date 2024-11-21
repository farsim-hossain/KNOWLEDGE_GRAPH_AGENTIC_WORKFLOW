from player_analysis_crew_groq import PlayerAnalysisCrew

from dotenv import load_dotenv
import os

load_dotenv()

def main():
    neo4j_uri = os.getenv('neo4j_uri')
    neo4j_user = os.getenv('neo4j_user')
    neo4j_password = os.getenv('neo4j_password')

    analysis_system = PlayerAnalysisCrew(
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password
    )
    
    results = analysis_system.analyze_performance()
    return results

if __name__ == "__main__":
    results = main()
    print("Crew AI + Groq Analysis Results:", results)



