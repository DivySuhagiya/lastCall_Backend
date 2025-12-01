# Last Call - Agentic Intelligence Backend 🧠

This is the backend service for **Last Call**, an immersive 3D murder mystery interrogation game. It is built using **FastAPI** and the **Google Gen AI Agent Development Kit (ADK)**.

The backend acts as the "Brain" of the operation, managing game sessions, maintaining conversation history, and dynamically engineering prompts for the Gemini 1.5 Flash model based on the game state (e.g., who is the killer vs. who is innocent).

---

## ✨ Features

- **Stateful Sessions**: Uses `InMemorySessionService` to track unique game states (Target, Killer, History) for every connected user.
- **Dynamic Prompt Injection**: Real-time Context Compaction in `prompt_builder.py` ensures the AI never hallucinates guilt if it is assigned an "Innocent" role.
- **Gemini 2.5 Integration**: Leverages the latest Gemini models for high-speed reasoning and natural language generation.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **AI Engine**: Google Gemini 2.5 Flash
- **Agent Framework**: Google Agent Development Kit (ADK)
- **Server**: Uvicorn

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API Key ([Get it from Google AI Studio](https://aistudio.google.com/))

### 1. Installation

**Create a virtual environment:**
```bash
# Windows
uv venv venv
.venv\Scripts\activate

# Mac/Linux
uv venv .venv
source venv/bin/activate
```

**Install dependencies:**
```bash
uv sync
```

### 2. Environment Configuration

**Create a `.env` file in the root directory:**
```bash
touch .env
```

**Add your configuration:**
```env
# Required: Your Google Gemini API Key
GOOGLE_API_KEY=your_actual_api_key_here

# Optional: Frontend URL for CORS (Defaults to * if empty)
FRONTEND_URL=http://localhost:5173
```

### 3. Running the Server

**Start the application:**
```bash
cd lastcall_agent
fastapi dev agent.py  # development mode
fastapi run agent.py  # production mode
```

The server will start at `http://localhost:8000`.

---

## 🔌 API Endpoints

### 1. Create Session

Initializes a new game state. Randomly assigns roles (Target/Killer) on the client side and stores them here.

- **URL**: `/create_session`
- **Method**: `POST`
- **Body**:
```json
{
  "user_id": "user_123",
  "session_id": "uuid_v4",
  "target": "amelia",
  "killer": "sebastian"
}
```

### 2. Chat

Sends a user message to the agent and retrieves the response.

- **URL**: `/chat`
- **Method**: `POST`
- **Body**:
```json
{
  "app_name": "lastCall",
  "user_id": "user_123",
  "session_id": "uuid_v4",
  "message": "Where were you at 8:45 PM?"
}
```

- **Response**:
```json
{
  "responses": [
    {
      "text": "I was in my room reading. Ask the maid.",
      "role": "agent"
    }
  ]
}
```

### 3. Delete Session

Cleans up memory when the user disconnects or restarts.

- **URL**: `/delete_session`
- **Method**: `POST`

---

## 📂 Project Structure
```
.
├── lastcall_agent/
│   ├── prompt_builder.py   # 🧠 Core Logic: Dynamic Scenario Generators
│   ├── schemas.py          # Pydantic models for API requests
│   ├── agent.py            # FastAPI application entry point
└── .env                    # Environment secrets
```

---

## ⚠️ Deployment Note (Render/Cloud Run)

If deploying to a serverless platform (like Render Free Tier):

- The service may spin down after inactivity.
- **Cold Start**: The first request might take 45-60 seconds to process while the container boots. Subsequent requests will be fast.

---

## 📄 License

MIT License
