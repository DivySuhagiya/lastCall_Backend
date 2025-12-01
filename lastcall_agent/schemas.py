from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Represents a chat request.

    Attributes:
        app_name (str): The name of the application.
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
        message (str): The details of the message.
    """

    app_name: str
    user_id: str
    session_id: str
    message: str


class CreateSessionRequest(BaseModel):
    """
    Represents a create session request.

    Attributes:
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
        target (str): The target of the interrogation.
        killer (str): The name of the killer.
    """

    user_id: str
    session_id: str
    target: str
    killer: str

class DeleteSessionRequest(BaseModel):
    """
    Represents a delete session request.

    Attributes:
        user_id (str): The ID of the user.
        session_id (str): The ID of the session.
    """

    user_id: str
    session_id: str