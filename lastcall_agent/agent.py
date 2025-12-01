from google.adk.agents.llm_agent import Agent
from lastcall_agent.prompt_builder import build_prompt

import os
import logging

from time import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part

from dotenv import load_dotenv

from .schemas import ChatRequest
from .schemas import CreateSessionRequest
from .schemas import DeleteSessionRequest

from .character_agents.amelia.agent import amelia
from .character_agents.lucian.agent import lucian
from .character_agents.sebastian.agent import sebastian

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
service = InMemorySessionService()

load_dotenv()

origins = os.getenv("FRONTEND_URL")

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
    description='An character agent in the "last call" interrogation game. Who answer user\'s questions',
)


@app.post("/create_session")
async def create_session(request: CreateSessionRequest) -> dict:
    """
    Create a new session.

    Args:
        request (CreateSessionRequest): The request object containing the user_id, session_id, target, and killer.

    Returns:
        dict: A dictionary containing the session_id and user_id.

    """

    state_context = {
        "target": request.target,
        "killer": request.killer
    }

    session = await service.create_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id,
        state=state_context
    )

    logger.info("--- Session Properties ---")
    logger.info("ID (`id`):                %s", session.id)
    logger.info("Application Name (`app_name`): %s", session.app_name)
    logger.info("User ID (`user_id`):         %s", session.user_id)
    logger.info("Session State (`state`):     %s", session.state)
    logger.info("---------------------------------")

    return {"session_id": session.id, "user_id": session.user_id}


@app.post("/chat")
async def chat(request: ChatRequest) -> dict:
    """
    Chat with the agent.

    Args:
        request (ChatRequest): The request object containing the app_name, user_id, session_id, and message.

    Returns:
        dict: A dictionary containing the responses from the agent.

    """

    # Retrieve the session from the service.
    app_name = request.app_name
    user_id = request.user_id
    session_id = request.session_id
    retrieved_session = await service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    target = retrieved_session.state['target']
    killer = retrieved_session.state['killer']

    instruction = build_prompt(character_name=target, killer=killer)

    logger.info("instruction: %s", instruction)

    root_agent.instruction = instruction

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

    end_time = time()
    logger.info("Execution time: %.2fs", end_time - start_time)

    return {"responses": responses}


@app.post("/delete_session")
async def delete_session(request: DeleteSessionRequest) -> dict:
    """
    Delete a session.

    Args:
        request (DeleteSessionRequest): The request object containing the user_id and session_id.

    Returns:
        dict: A dictionary containing a message indicating that the session has been deleted.

    """

    await service.delete_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id
    )

    return {"message": "session deleted"}
