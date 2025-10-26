print("✅ ai_agent.py executing")

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage

# ✅ Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

print("OPENAI_API_KEY loaded:", bool(OPENAI_API_KEY))
print("GROQ_API_KEY loaded:", bool(GROQ_API_KEY))
print("TAVILY_API_KEY loaded:", bool(TAVILY_API_KEY))

# ✅ Unified response function
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    print("🚀 get_response_from_ai_agent called")
    print(f"Model: {llm_id}, Provider: {provider}, WebSearch: {allow_search}")

    # Choose LLM
    if provider.lower() == "groq":
        llm = ChatGroq(model=llm_id)
    elif provider.lower() == "openai":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError("Unsupported provider")

    # Add search tools if allowed
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # ✅ Create the agent (new API — no state_modifier)
    agent = create_react_agent(
    model=llm,
    tools=tools,
    )
    agent.update_state({"system_prompt": system_prompt})


    # ✅ Include the system prompt in the first message
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    # ✅ Invoke the agent using the new interface
    print("🧠 Invoking agent...")
    response = agent.invoke({"messages": messages})
    messages = response.get("messages", [])
    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]

    if ai_messages:
        print("✅ Agent responded successfully!")
        return ai_messages[-1]
    else:
        print("⚠️ No response generated.")
        return "No response generated."
