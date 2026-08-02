from fastapi import FastAPI, Request
from langserve import add_routes
import uvicorn

from tools.memory_tool import agent_with_history

app = FastAPI(
    title="AntiLiso-AI Server",
    version="1.0",
    description="AntiLiso-AI Server",
)

add_routes(
    app,
    agent_with_history,
    path="/antiliso",
    config_keys=["configurable"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)