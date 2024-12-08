from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict
import asyncio
from backend.agent import create_agent
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: Dict):
    try:
        message = request.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        agent = create_agent()
        
        async def event_generator():
            async for event in agent.stream_run(message):
                if event.get("type") == "tool_start":
                    # Stream tool call information
                    yield json.dumps({
                        "type": "tool_call",
                        "content": {
                            "tool": event.get("tool"),
                            "input": event.get("input")
                        }
                    }) + "\n"
                elif event.get("type") == "llm":
                    # Stream LLM response
                    yield json.dumps({
                        "type": "message",
                        "content": event.get("content", "")
                    }) + "\n"

        return EventSourceResponse(event_generator())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
