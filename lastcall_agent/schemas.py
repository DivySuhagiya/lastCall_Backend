from pydantic.fields import Field
from pydantic.types import conlist
from pydantic import BaseModel


class Evidence(BaseModel):
    """
    Represents a piece of evidence in the murder mystery.

    Attributes:
        name (str): The name/title of the evidence.
        description (str): Detailed description of the evidence and its relevance to the case.
    """
    name: str
    description: str


class SuspectCharacter(BaseModel):
    """
    Represents a suspect character in the murder mystery.

    Attributes:
        name (str): The character's full name.
        gender (str): The character's gender (male/female).
        description (str): Character background, personality traits, and role in the story.
    """
    name: str
    gender: str
    description: str


class MurderMysteryStory(BaseModel):
    """
    Complete murder mystery story structure with all essential elements.

    Attributes:
        victim (str): Name of the victim.
        killer (str): Name of the killer (one of the suspects).
        story (str): The complete narrative of the murder mystery.
        location (str): The location where the murder took place.
        character_details (list[SuspectCharacter]): Exactly 3 suspect characters (1 female, 2 males).
        evidences (list[Evidence]): Exactly 3 pieces of evidence that help solve the mystery.
    """
    victim: str
    killer: str
    story: str
    location: str
    character_details: conlist(SuspectCharacter, min_length=3, max_length=3)
    evidences: conlist(Evidence, min_length=3, max_length=3)


class GenerateStoryRequest(BaseModel):
    """
    Request schema for story generation endpoint.

    Attributes:
        app_name (str): The application name (should be "lastCall").
        user_id (str): Unique identifier for the user.
        session_id (str): Unique identifier for the session.
    """
    app_name: str
    user_id: str
    session_id: str


class CharacterScenario(BaseModel):
    """
    Represents a character's role-play scenario/instruction.

    Attributes:
        name (str): The character's name (must match a suspect from the story).
        scenario (str): Detailed role-play instructions including role, key facts, and conversation guidelines.
    """
    name: str
    scenario: str


class CharacterScenariosOutput(BaseModel):
    """
    Collection of character scenarios for all suspects.

    Attributes:
        scenarios (list[CharacterScenario]): Exactly 3 character scenarios matching the 3 suspects.
    """
    scenarios: conlist(CharacterScenario, min_length=3, max_length=3) = Field(
        ...,
        description="Exactly three scenarios with the same schema."
    )


class EvidenceImagePrompt(BaseModel):
    """
    Image generation prompt for a piece of evidence.

    Attributes:
        name (str): Name of the evidence (must match evidence from story).
        image_prompt (str): Detailed prompt for AI image generation describing the evidence visually.
    """
    name: str
    image_prompt: str


class EvidenceImagePromptsOutput(BaseModel):
    """
    Collection of image generation prompts for all evidence.

    Attributes:
        prompts (list[EvidenceImagePrompt]): Exactly 3 image prompts for the 3 pieces of evidence.
    """
    prompts: conlist(EvidenceImagePrompt, min_length=3, max_length=3)


class GeneratedEvidenceImage(BaseModel):
    """
    Generated image URL for a piece of evidence.

    Attributes:
        name (str): Name of the evidence.
        url (str): URL of the generated evidence image.
    """
    name: str
    url: str


class EvidenceImagesOutput(BaseModel):
    """
    Collection of generated image URLs for all evidence.

    Attributes:
        urls (list[GeneratedEvidenceImage]): Exactly 3 generated image URLs for the evidence.
    """
    urls: conlist(GeneratedEvidenceImage, min_length=3, max_length=3)


class ChatRequest(BaseModel):
    """
    Represents a chat request.

    Attributes:
        app_name (str): The name of the application.
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
        victim_name (str): The name of the victim.
        character_name (str): The name of the character.
        instructions (str): The instructions for the agent.
        message (str): The details of the message.
    """

    app_name: str
    user_id: str
    session_id: str
    victim_name: str
    character_name: str
    instructions: str
    message: str


class CreateSessionRequest(BaseModel):
    """
    Represents a create session request.

    Attributes:
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
    """

    user_id: str
    session_id: str


class DeleteSessionRequest(BaseModel):
    """
    Represents a delete session request.

    Attributes:
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
    """

    user_id: str
    session_id: str
