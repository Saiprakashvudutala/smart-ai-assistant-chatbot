print("✅ Step 1: backend.py started executing")

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    from typing import List
    from ai_agent import get_response_from_ai_agent
    print("✅ Step 2: All imports successful")
except Exception as e:
    print("❌ Import error:", e)
    raise

# ✅ Define FastAPI app
app = FastAPI(title="LangGraph AI Agent API")
print("✅ Step 3: FastAPI app created")

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.get("/")
def root():
    print("✅ Step 4: Root endpoint called")
    return {"message": "✅ FastAPI backend is running!"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Step 5: Starting FastAPI backend on http://127.0.0.1:9999 ...")
    uvicorn.run(app, host="127.0.0.1", port=9999, reload=False)
