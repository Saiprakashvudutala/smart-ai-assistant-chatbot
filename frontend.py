import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot Agents", page_icon="🤖", layout="centered")

st.title("AI Chatbot Agents")
st.markdown("Create and interact with AI Agents powered by LangGraph!")

system_prompt = st.text_area("Define your AI Agent:", "You are a smart assistant that answers clearly and briefly.")


provider = st.radio("Select Provider:", ["Groq", "OpenAI"])
provider = provider.lower()

model_name = None
if provider == "groq":
    model_name = st.selectbox("Select Groq Model:", ["llama-3.3-70b-versatile", "mixtral-8x7b"])
elif provider == "openai":
    model_name = st.selectbox("Select OpenAI Model:", ["gpt-4o-mini", "gpt-4o"])

allow_web_search = st.checkbox("Allow Web Search")

query = st.text_area("Enter your query:", "Ask Anything!")

if st.button("Ask Agent!"):
    with st.spinner("Thinking..."):
        data = {
            "provider": provider,
            "model_name": model_name,
            "system_prompt": system_prompt,
            "query": query,
            "allow_search": allow_web_search
        }

        try:
            response = requests.post("http://127.0.0.1:9999/chat", json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                st.markdown("### Agent Response")
                st.write(result.get("response", "No response from agent"))
            else:
                st.error(f"Request failed with status {response.status_code}")
        except Exception as e:
            st.error(f"Connection Error: {e}")




