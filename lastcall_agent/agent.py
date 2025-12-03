from lastcall_agent.schemas import GenerateStoryRequest
from lastcall_agent.sub_agents.evidence_prompt_agent import evidence_prompt_agent
from lastcall_agent.sub_agents.evidence_image_generator_agent import evidence_image_generator_agent
from lastcall_agent.sub_agents.scenario_builder_agent import scenario_builder_agent
from lastcall_agent.sub_agents.story_agent import story_agent

from google.adk.agents.sequential_agent import SequentialAgent
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
service = InMemorySessionService()

load_dotenv()

# origins = os.getenv("FRONTEND_URL")
origins = ["*"]

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Agent ====================
story_generation_pipeline = SequentialAgent(
    name='story_generation_pipeline',
    description='Orchestrates the complete story generation workflow: story → scenarios → evidence prompts → evidence images.',
    sub_agents=[
        story_agent,
        scenario_builder_agent,
        evidence_prompt_agent,
        evidence_image_generator_agent
    ]
)

interrogation_agent = Agent(
    name='interrogation_agent',
    description='A suspect character in the "Last Call" interrogation game who responds to player questions.',
    model='gemini-2.5-flash-lite',
)


# ==================== API Endpoints ====================

@app.post("/create_session")
async def create_session(request: CreateSessionRequest) -> dict:
    """
    Create a new game session for a user.
    
    This endpoint initializes a new session in the in-memory session service,
    which will store conversation history and game state.
    
    Args:
        request (CreateSessionRequest): Contains user_id and session_id.
    
    Returns:
        dict: A dictionary with:
            - session_id (str): The created session identifier
            - user_id (str): The user identifier
    
    Example:
        Request:
        ```
        {
            "user_id": "user_123",
            "session_id": "session_abc"
        }
        ```
        
        Response:
        ```
        {
            "session_id": "session_abc",
            "user_id": "user_123"
        }
        ```
    """
    session = await service.create_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id,
    )

    logger.info("--- Session Properties ---")
    logger.info("ID (`id`):                %s", session.id)
    logger.info("Application Name (`app_name`): %s", session.app_name)
    logger.info("User ID (`user_id`):         %s", session.user_id)
    logger.info("---------------------------------")

    return {"session_id": session.id, "user_id": session.user_id}


@app.post("/create_story")
async def generate_story(request: GenerateStoryRequest) -> dict:
    """
    Generate a complete murder mystery story with suspects, evidence, and character scenarios.
    
    This endpoint orchestrates multiple AI agents to:
    1. Generate a murder mystery plot
    2. Create role-play scenarios for each suspect
    3. Generate image prompts for evidence
    4. Create evidence images
    
    Args:
        request (GenerateStoryRequest): Contains app_name, user_id, and session_id.
    
    Returns:
        dict: A dictionary containing:
            - generated_story (dict): Complete murder mystery with victim, killer, suspects, location, and evidence
            - generated_scenarios (dict): Role-play instructions for each suspect character
            - generated_evidence_prompts (dict): Image generation prompts for evidence
            - generated_evidence_urls (str): JSON string with generated image URLs
    
    Raises:
        Exception: If story generation fails or session is invalid.
    
    Example:
        Request:
        ```
        {
            "app_name": "lastCall",
            "user_id": "user_123",
            "session_id": "session_abc"
        }
        ```
        
        Response:
        ```
        {
            "generated_story": {
                "victim": "Arthur Pendelton",
                "killer": "Eleanor Vance",
                "story": "...",
                "location": "...",
                "character_details": [...],
                "evidences": [...]
            },
            "generated_scenarios": {
                "scenarios": [...]
            },
            "generated_evidence_prompts": {
                "prompts": [...]
            },
            "generated_evidence_urls": "..."
        }
        ```
    """
    runner = Runner(
        app_name="lastCall",
        agent=story_generation_pipeline,
        session_service=service,
    )

    generated_image_urls = ""
    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=request.session_id,
        new_message=Content(
            parts=[Part(text="Generate a murder mystery plot.")],
            role="user",
        )
    ):
        if event.content and event.is_final_response():
            generated_image_urls = event.content.parts[0].text

    session = await service.get_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id
    )
    
    logger.info("Session state: %s", session.state)

    return {
        "generated_story": session.state['generated_story'],
        "generated_scenarios": session.state['generated_scenarios'],
        "generated_evidence_prompts": session.state['generated_evidence_prompts'],
        "generated_evidence_urls": generated_image_urls
    }


@app.post("/chat")
async def chat(request: ChatRequest) -> dict:
    """
    Handle interrogation chat between player and suspect character.
    
    The player asks questions to a suspect, and the AI agent responds in character
    based on their assigned scenario and role in the murder mystery.
    
    Args:
        request (ChatRequest): Contains:
            - app_name (str): Application identifier
            - user_id (str): User identifier
            - session_id (str): Session identifier
            - victim_name (str): Name of the victim
            - character_name (str): Name of the suspect being interrogated
            - instructions (str): Character's role-play scenario
            - message (str): Player's question/message
    
    Returns:
        dict: A dictionary containing:
            - responses (list): List of agent responses with text and role
    
    Example:
        Request:
        ```
        {
            "app_name": "lastCall",
            "user_id": "user_123",
            "session_id": "session_abc",
            "victim_name": "Arthur Pendelton",
            "character_name": "Eleanor Vance",
            "instructions": "[ROLE: You are the killer...]",
            "message": "Where were you on the night of the murder?"
        }
        ```
        
        Response:
        ```
        {
            "responses": [
                {
                    "text": "I was working late in my office...",
                    "role": "agent"
                }
            ]
        }
        ```
    """
    # Build character-specific prompt
    instructions = build_prompt(
        request.victim_name,
        request.character_name,
        request.instructions
    )

    logger.info("Character instructions: %s", instructions)

    # Set agent instruction dynamically for this character
    interrogation_agent.instruction = instructions

    start_time = time()
    runner = Runner(
        app_name="lastCall",
        agent=interrogation_agent,
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
    logger.info("Interrogation response time: %.2fs", end_time - start_time)

    return {"responses": responses}


@app.post("/delete_session")
async def delete_session(request: DeleteSessionRequest) -> dict:
    """
    Delete an existing game session and all associated data.
    
    This clears the conversation history and game state from memory.
    Use this when a player finishes the game or wants to start fresh.
    
    Args:
        request (DeleteSessionRequest): Contains user_id and session_id to delete.
    
    Returns:
        dict: A confirmation message indicating successful deletion.
    
    Example:
        Request:
        ```
        {
            "user_id": "user_123",
            "session_id": "session_abc"
        }
        ```
        
        Response:
        ```
        {
            "message": "session deleted"
        }
        ```
    """
    await service.delete_session(
        app_name="lastCall",
        user_id=request.user_id,
        session_id=request.session_id
    )

    return {"message": "session deleted"}
