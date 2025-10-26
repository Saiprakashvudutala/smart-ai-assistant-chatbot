print("backend.py is executing")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from ai_agent import get_response_from_ai_agent

app = FastAPI(title="LangGraph AI Agent API")

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.get("/")
def root():
    print("Root endpoint called")
    return {"message": "FastAPI backend is running!"}

@app.post("/chat")
@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        print("Incoming request data:", data)

        response = get_response_from_ai_agent(
            model_name=data.get("model_name"),
            provider=data.get("provider"),
            allow_search=data.get("allow_search"),
            query=data.get("query"),
            system_prompt=data.get("system_prompt")
        )

        print("Agent response generated successfully")
        return {"response": response}

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Backend Error:", str(e))
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    print("Starting backend on http://127.0.0.1:9999 ...")
    uvicorn.run(app, host="127.0.0.1", port=9999, reload=False)

