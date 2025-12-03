# Last Call: The Infinite Murder Mystery Engine 🧠🕵️‍♂️

> **Backend Service**  
> **Powered by:** Google Gen AI ADK & Gemini 2.5 Flash Lite

This is the backend engine for **Last Call**, a fully procedural murder mystery game. Unlike traditional games with pre-written scripts, this system uses a **Sequential Multi-Agent Pipeline** to generate unique plots, suspect profiles, and evidence assets in real-time.

It orchestrates a team of specialized AI agents (Storyteller, Profiler, Visualizer) to ensure every game session is unique, coherent, and infinitely replayable.

---

## ✨ Features

- **Sequential Agent Pipeline**: A chain of 4 specialized agents working in harmony:
  1. **Story Agent**: Writes the plot (Victim, Killer, Motive).
  2. **Scenario Builder**: Generates system prompts for 3 unique suspects.
  3. **Evidence Designer**: Identifies physical clues and writes visual prompts.
  4. **Visualizer**: Generates image assets for the evidence using tools.
- **Infinite Replayability**: No two playthroughs are the same. The "Truth" is generated from scratch every time you start a story.
- **Stateful Intelligence**: Uses `InMemorySessionService` to persist the procedurally generated world state (Target, Killer, Plot) across the user's session.
- **Structured Output**: Leverages **Pydantic** to enforce strict JSON schemas between agents, ensuring the pipeline never breaks.

---

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **AI Engine**: Google Gemini 2.5 Flash Lite
- **Agent Framework**: Google Gen AI Agent Development Kit (ADK)
- **Package Manager**: uv
- **Server**: Uvicorn

---

## 📂 Project Structure

```text
.
├── lastcall_agent/
│   ├── sub_agents/                 # 🧠 Specialized Agent Logic
│   │   ├── evidence_image_generator_agent.py
│   │   ├── evidence_prompt_agent.py
│   │   ├── scenario_builder_agent.py
│   │   └── story_agent.py
│   ├── tools/                      # 🛠️ Agent Tools (Function Calling)
│   │   └── generate_image.py
│   ├── agent.py                    # 🚀 Main FastAPI Application & Pipeline Config
│   ├── prompt_builder.py           # Context Injection Logic
│   ├── schemas.py                  # Pydantic Data Models
│   └── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml                  # Dependency Configuration
├── README.md
└── uv.lock                         # Lockfile for reproducible builds
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- `uv` installed ([Recommended for speed](https://github.com/astral-sh/uv))
- A Google Gemini API Key ([Get it from Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Installation

This project uses `uv` for blazing-fast dependency management.

**Clone and Sync:**

```bash
# Clone the repository
git clone https://github.com/DivySuhagiya/lastCall_Backend.git
cd lastCall_Backend

# Create virtual env and install dependencies
uv sync
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
touch .env
```

Add your configuration:

```env
# Required: Your Google Gemini API Key
GOOGLE_API_KEY=your_actual_api_key_here

# Optional: Frontend URL for CORS (Defaults to * if empty)
FRONTEND_URL=http://localhost:5173
```

### 3. Running the Server

Start the application using `fastapi`:

```bash
fastapi dev agent.py
```

The server will start at `http://localhost:8000`.

---

## 🔌 API Endpoints

### 1. Create Session

Initializes the memory service for the user. This must be called before generating a story.

- **URL**: `/create_session`
- **Method**: `POST`
- **Body**:

```json
{
  "user_id": "user_123",
  "session_id": "uuid_v4"
}
```

### 2. Generate Story (The Engine)

Triggers the Sequential Agent Pipeline. This creates the world state (Plot, Suspects, Evidence).  
⚠️ **Note**: This may take 5-10 seconds to complete.

- **URL**: `/create_story`
- **Method**: `POST`
- **Body**:

```json
{
  "app_name": "lastCall",
  "user_id": "user_123",
  "session_id": "uuid_v4"
}
```

- **Response**: Returns the full `generated_story`, `generated_scenarios` (for the characters), and `generated_evidence_urls`.

### 3. Chat (Interrogation)

Talk to a specific suspect. The frontend must pass the character's generated "instructions" (from the `/create_story` response) so the agent knows who to roleplay.

- **URL**: `/chat`
- **Method**: `POST`
- **Body**:

```json
{
  "app_name": "lastCall",
  "user_id": "user_123",
  "session_id": "uuid_v4",
  "victim_name": "Arthur Pendelton",
  "character_name": "Amelia",
  "instructions": "[ROLE: You are the killer...]",
  "message": "Where were you at 8:00 PM?"
}
```

### 4. Delete Session

Cleans up memory when the user disconnects or restarts.

- **URL**: `/delete_session`
- **Method**: `POST`

---

## ⚠️ Deployment Note (Render/Cloud Run)

If deploying to a serverless platform (like Render Free Tier):

- The service may spin down after inactivity.
- **Cold Start**: The first request might take 45-60 seconds to process while the container boots. Subsequent requests will be fast.

---

## 📄 License

MIT License
