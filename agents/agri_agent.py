from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_core.chat_history import InMemoryChatMessageHistory
from utils.llm_loader import load_llm
from tools.web_scraper_tool import web_scraper_tool
from tools.document_tool import document_search_tool
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the shape of the state
class AgentState(TypedDict):
    input: str
    result: str
    chat_history: Annotated[list, add_messages]

# Store chat histories
chat_histories = {}

def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

def get_agri_agent():
    llm = load_llm()
    tools = [web_scraper_tool(), document_search_tool()]

    base_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    # Define the agent
    agent_executor = RunnableWithMessageHistory(
        runnable=RunnableLambda(lambda x: base_agent.invoke(x)),
        get_session_history=get_chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    # Define the graph
    builder = StateGraph(AgentState)

    builder.add_node("start", RunnablePassthrough())
    builder.add_node("agent_executor", agent_executor)

    builder.set_entry_point("start")
    builder.add_edge("start", "agent_executor")
    builder.add_edge("agent_executor", END)

    graph = builder.compile()

    # Wrap in a simple callable to return result and chat_history
    def run_agent(input_text: str, session_id: str):
        modified_input = f"User: {input_text}\nPlease respond in the same language as the question."

        final_state = graph.invoke(
            {"input": modified_input},
            config={"configurable": {"session_id": session_id}}
        )

        # Always retrieve chat history from memory
        history = get_chat_history(session_id).messages

        return {
            "result": final_state.get("result", ""),
            "chat_history": history
        }

    return run_agent
