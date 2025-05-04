from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from utils.llm_loader import load_llm
from tools.web_scraper_tool import web_scraper_tool
from tools.document_tool import document_search_tool

# Store chat histories
chat_histories = {}

def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

def get_agri_agent():
    llm = load_llm()
    tools = [web_scraper_tool(), document_search_tool()]
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        ),
        tools=tools,
        verbose=True
    )
    agent_with_history = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=get_chat_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    return agent_with_history
