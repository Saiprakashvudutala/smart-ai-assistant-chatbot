import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

print("ai_agent.py executing")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

print(f"OPENAI_API_KEY loaded: {bool(OPENAI_API_KEY)}")
print(f"GROQ_API_KEY loaded: {bool(GROQ_API_KEY)}")
print(f"TAVILY_API_KEY loaded: {bool(TAVILY_API_KEY)}")


def get_response_from_ai_agent(provider, model_name, query, system_prompt, allow_search=False):
    """
    Handles AI agent response logic for both OpenAI and Groq providers.
    Supports optional web search using Tavily.
    """
    print("get_response_from_ai_agent called")
    print(f"Model: {model_name}, Provider: {provider}, WebSearch: {allow_search}")

    try:
        if not provider or not model_name:
            raise ValueError("Provider or model_name is missing!")

        if provider.lower() == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set in .env")
            llm = ChatOpenAI(model=model_name, api_key=OPENAI_API_KEY)

        elif provider.lower() == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is not set in .env")
            llm = ChatGroq(model=model_name, api_key=GROQ_API_KEY)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

        tools = [TavilySearchResults(max_results=2)] if allow_search else []

        agent = create_react_agent(model=llm, tools=tools)

        print("Invoking agent...")

        response = agent.invoke({
            "messages": [
                ("system", system_prompt or "You are a helpful assistant."),
                ("user", query)
            ]
        })

        if isinstance(response, dict):
            messages = response.get("messages", [])
            if messages and hasattr(messages[-1], "content"):
                print("Agent response received successfully!")
                return messages[-1].content

        print("No valid content in agent response:", response)
        return "No valid response from the agent."

    except Exception as e:
        print("Agent Error:", str(e))
        return f"Agent Error: {str(e)}"

if __name__ == "__main__":
    result = get_response_from_ai_agent(
        provider="groq",
        model_name="llama-3.3-70b-versatile",
        query="Who is the president of India in 2025?",
        system_prompt="You are a smart assistant that answers clearly and briefly.",
        allow_search=False
    )
    print("\n Final Output:", result)











