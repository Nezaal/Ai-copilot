from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType
from backend.llm_config import get_llm
from backend.engine import get_chat_response

search_tool = DuckDuckGoSearchRun()

# This is the "Aha!" moment: We give the agent eyes (PDF) and hands (Web)
pdf_tool = Tool(
    name="PDF_Search",
    func=lambda q: get_chat_response(q),
    description="Useful for when you need to answer questions about the uploaded PDF document."
)

def get_agent_response(query, use_cloud=True):
    llm = get_llm(use_cloud=use_cloud)
    agent = initialize_agent(
        tools=[search_tool, pdf_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent.run(query)
