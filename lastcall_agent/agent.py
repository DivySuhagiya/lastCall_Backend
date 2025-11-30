from google.adk.agents.run_config import StreamingMode
from google.adk.agents.run_config import RunConfig
from time import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents.llm_agent import Agent
from google.genai.types import Content, Part

from dotenv import load_dotenv


from .character_agents.amelia.agent import amelia
from .character_agents.lucian.agent import lucian
from .character_agents.sebastian.agent import sebastian

app = FastAPI()
service = InMemorySessionService()
load_dotenv()


class MessageDetails(BaseModel):
    target: str
    message: str


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: MessageDetails


class SessionRequest(BaseModel):
    user_id: str
    session_id: str


origins = ["http://localhost:5173"]

# Cors config


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description='An agent that orchestrates the "last call" interrogation game.',
    instruction='''
## 1. YOUR IDENTITY & GOAL ##
You are the **Orchestrator** for the "Last Call" interrogation game. You are not a character; you are the logical controller. Your primary job is to receive a JSON request from the user, check it against the game's rules, and then call the correct Sub-Agent (Amelia, Lucian, or Sebastian) using the provided tools.

## 2. USER INPUT FORMAT ##
The user's input will **always** be a JSON object with a "target" and a "message".
* **Example 1 (Interrogation):** `{"target": "Amelia", "message": "How are you today?"}`

## 3. AGENT CALL ##
You must call the correct Sub-Agent (Amelia, Lucian, or Sebastian) using the provided subagents and pass the only message.

You never produce any output. You only call the Sub-Agent.
    ''',
    sub_agents=[amelia, lucian, sebastian]
)


@app.post("/create_session")
async def create_session(request: SessionRequest):
    session = await service.create_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id
    )

    print(f"--- Examining Session Properties ---")
    print(f"ID (`id`):                {session.id}")
    print(f"Application Name (`app_name`): {session.app_name}")
    print(f"User ID (`user_id`):         {session.user_id}")
    print(f"---------------------------------")

    return {"session_id": session.id, "user_id": session.user_id}


@app.post("/chat")
async def chat(request: ChatRequest):
    # print start time
    start_time = time()
    runner = Runner(
        app_name="lastCall",
        agent=root_agent,
        session_service=service,
    )

    user_message = Content(
        parts=[Part(text=str(request.message))],
        role="user",
    )

    responses = []
    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=request.session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content:
            responses.append({
                "text": event.content.parts[0].text,
                "role": "agent"
            })

    # print end time
    end_time = time()
    print(f"Execution time: {end_time - start_time} seconds")

    return {"responses": responses}


@app.post("/delete_session")
async def delete_session(request: SessionRequest):
    await service.delete_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id
    )

    return {"session deleted"}
