# This file will be created by the user during Phase 3.
# It will contain the Multi-Agent Crew logic.
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool("DuckDuckGoSearch")
def search_tool(query: str):
    """Search the web for information about current events or specific topics. 
    Pass a simple text query."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            # We limit results to 3 to keep the local model focused
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No results found. Try a different query."
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception as e:
        # If we hit rate limits, we tell the agent to wait
        print(f"⚠️ Search error: {e}")
        return "Search is currently busy or rate-limited. Please use your existing knowledge or try one more time."

def get_crew_llm():
    # 🚨 For CrewAI, we use their native LLM class to avoid LiteLLM provider errors
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return LLM(
            model="openrouter/google/gemma-2-9b-it",
            api_key=api_key
        )
    # Default: Local Ollama with provider prefix
    return LLM(
        model="ollama/gemma2:2b",
        base_url="http://localhost:11434"
    )

def run_crew_task(topic):
    llm = get_crew_llm()

    # 1. Define Agents
    researcher = Agent(
        role='Researcher',
        goal=f'Find 3 groundbreaking facts about {topic}',
        backstory="You are an elite researcher who finds the truth no matter what.",
        tools=[search_tool],
        llm=llm,
        allow_delegation=False
    )

    writer = Agent(
        role='Content Creator',
        goal=f'Write a viral Gen-Z style LinkedIn post about {topic}',
        backstory="You turn boring data into viral content using emojis and slang.",
        llm=llm,
        allow_delegation=False
    )

    # 2. Define Tasks
    task1 = Task(
        description=f"Research {topic}", 
        agent=researcher,
        expected_output="A list of 3 groundbreaking facts about the topic."
    )
    task2 = Task(
        description=f"Write post about {topic}", 
        agent=writer,
        expected_output="A viral, emoji-rich LinkedIn post summarizing the research findings."
    )

    # 3. Assemble the Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=True,
        process=Process.sequential
    )

    result = crew.kickoff()
    return result.raw if hasattr(result, 'raw') else str(result)
