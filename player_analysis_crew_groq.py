from langchain_groq import ChatGroq
from crewai import Task, Crew, Agent, Process
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')


class PlayerAnalysisCrew:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        # Updated LLM configuration for Groq
        self.llm = ChatGroq(
            model_name="groq/mixtral-8x7b-32768",  # Updated model name
            temperature=0,
            groq_api_key=os.environ["GROQ_API_KEY"]
        )
        
        # Configure agents with the correct LLM setup
        self.analyst = Agent(
            role="Performance Analyst",
            goal="Analyze player performance patterns and metrics",
            backstory="Expert in sports analytics with deep understanding of performance metrics",
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
        
        self.detective = Agent(
            role="Pattern Detective",
            goal="Identify complex performance patterns and trends",
            backstory="Specialized in detecting subtle changes in player development",
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
        
        self.advisor = Agent(
            role="Strategy Advisor",
            goal="Generate actionable recommendations",
            backstory="Expert in translating analysis into practical improvements",
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )

    def get_player_data(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Player)-[:HAS_STATE]->(s:PlayerState)
                WITH DISTINCT p, s
                LIMIT 10
                RETURN p.player_name, s.scoring_class, s.start_season, s.end_season
            """)
            return [dict(record) for record in result]

    def analyze_performance(self):
        player_data = self.get_player_data()
        
        analysis_task = Task(
            description=f"""Analyze performance metrics for all {len(player_data)} players in the dataset. 
                        Compare their scoring classes, identify group patterns, and highlight notable transitions 
                        across seasons. Consider the collective performance trends.""",
            expected_output="Comprehensive analysis of multiple players' performance patterns and group trends",
            agent=self.analyst
        )
        
        pattern_task = Task(
            description=f"""Detect patterns across {len(player_data)} players:
                        - Common performance trajectories
                        - Scoring class distributions
                        - Season-to-season changes
                        - Group performance indicators""",
            expected_output="Multi-player pattern analysis with comparative insights",
            agent=self.detective
        )
        
        strategy_task = Task(
            description=f"""Generate strategic recommendations based on the analysis of {len(player_data)} players:
                        - Team-level improvements
                        - Group-specific training strategies
                        - Performance optimization across different scoring classes
                        - Season-based preparation guidelines""",
            expected_output="Strategic recommendations for team and group performance improvements",
            agent=self.advisor
        )
        
        crew = Crew(
            agents=[self.analyst, self.detective, self.advisor],
            tasks=[analysis_task, pattern_task, strategy_task]
        )
        
        return crew.kickoff()