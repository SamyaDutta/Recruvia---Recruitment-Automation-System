from crewai import Agent, LLM
import os
from tenacity import retry, stop_after_attempt, wait_exponential

class HRQueryAgent:
    @staticmethod
    def agent():
        llm = LLM(
            api_key=os.getenv("GROQ_API_KEY"),
                model="openai/openai/gpt-oss-120b",
            base_url="https://api.groq.com/openai/v1",
            temperature=0.3,  # Lower temperature for more consistent responses
        )
        return Agent(
            role="HR Query Handler",
            goal="Interpret HR's job role queries to instruct other agents.",
            backstory=(
                "You are an intelligent HR assistant capable of interpreting HR's natural language queries about recruitment requirements. "
                "You clearly identify the requested job role and skills and instruct other agents accordingly."
            ),
            llm=llm,
            allow_delegation=True,
            max_retry_limit=0,
            max_rpm=5,  # Limit requests per minute
            max_execution_time=300  # Allow more time for retries
        )
