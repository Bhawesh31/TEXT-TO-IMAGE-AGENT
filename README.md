# AI Text-to-Image Generation Agent

## 🎯 Quick Start

```bash
docker-compose up
```

Access the API at `http://localhost:8000`

- API Docs: `http://localhost:8000/docs`

---

## 🏗️ Architecture

```
User Input
    ↓
FastAPI Backend (Port 8000)
    ├── POST /generate
    │   ├─→ LLM Agent (Prompt Enhancer)
    │   ├─→ Image Generator
    │   └─→ Vector Memory (Store)
    │
    └── POST /edit
        ├─→ Vector Memory (Retrieve Last)
        ├─→ Append User Modifications
        ├─→ Image Generator
        └─→ Vector Memory (Store)
```

---

## 🧩 Components

### Backend Structure

```
backend/
├── app.py              # FastAPI application, request routing
├── models.py           # Pydantic request/response schemas
├── llm.py              # Prompt enhancement logic (Art Director)
├── image.py            # Image generation with placeholder service
├── vector_db.py        # In-memory prompt storage & retrieval
├── config.py           # Environment configuration
├── utils.py            # Logging utilities
├── exceptions.py       # Custom exception classes
└── requirements.txt    # Python dependencies
```

### API Endpoints

#### POST /generate
**Create a new image from user input**

Request:
```json
{
  "user_input": "a sleek red sports car in neon city"
}
```

Response:
```json
{
  "prompt": "A sleek red sports car, futuristic neon city environment, cinematic lighting, 4K ultra-detailed, professional photography",
  "image_data": <image_content_or_reference>
}
```

#### POST /edit
**Modify the last generated image**

Request:
```json
{
  "edit_text": "make it sunset lighting"
}
```

Response:
```json
{
  "prompt": "A sleek red sports car in neon city, make it sunset lighting",
  "image_data": <image_content_or_reference>
}
```

---

## 🎨 Design Decisions

### 1. Why FastAPI?
- **Fast & Modern**: Built on async, Pydantic validation
- **Type Safe**: Automatic validation with type hints
- **Built-in Docs**: Auto-generated Swagger UI & ReDoc
- **Error Handling**: Structured exception management
- **Lightweight**: Minimal dependencies

### 2. Why Gemini API?
- **No Setup**: Free API key in seconds
- **Powerful**: Multi-modal (text & image in one API)
- **Cost**: Pay as you go, generous free tier
- **Easy Integration**: Simple Python client library
- **Real AI**: Not a placeholder, actual LLM/image generation

### 3. Why Supabase + In-Memory Fallback?
- **Primary (Supabase)**: Real PostgreSQL, not a mock
  - Persistent storage across restarts
  - Built-in backups & disaster recovery
  - Serverless: no infrastructure to manage
  - Free tier: 500MB storage, unlimited API calls
- **Fallback (In-Memory)**: Zero setup for quick prototyping
  - Works without any DB setup
  - Perfect for development/testing
  - Auto-switches if DB unavailable

**Architecture:**
```python
if SUPABASE_CONFIGURED:
    db = SupabaseDB()  # Production grade
else:
    db = PromptMemory()  # Development fallback
```

### 4. Why Modular Structure?
- **Separation of Concerns**: Each module has single job
- **Testability**: Easy to mock components
- **Maintainability**: Changes isolated to one file
- **Scalability**: Swap modules independently (e.g., new LLM provider)

---

## ⚙️ Trade-offs

### Gemini as Single Provider
- ⚠️ **Risk**: Vendor lock-in to Google's API
- ✅ **Benefit**: Integrated text + image, easy setup
- 🔄 **Mitigation**: Abstract in `llm.py` & `image.py`, can swap to OpenAI/Claude/Midjourney

### PostgreSQL + In-Memory Dual Strategy
- ✅ **Best of Both**: Production DB when available, fallback when not
- ✅ **Zero Lock-in**: Migrate away from Supabase anytime
- ✅ **Resilience**: App keeps working if DB is down

---

## 🐳 Docker & Deployment

### Docker Setup

- **Base**: Python 3.10 slim image
- **Server**: Uvicorn ASGI server
- **Port**: 8000 (configurable via environment)
- **Compose**: Single-service stack (ready for scaling)

### Environment Variables

Create a `.env` file:

```env
DEBUG=False
LOG_LEVEL=INFO
API_TIMEOUT=30
```

---

## 📦 Dependencies

| Package         | Purpose                            |
| --------------- | ---------------------------------- |
| `fastapi`       | Web framework for API              |
| `uvicorn`       | ASGI server                        |
| `pydantic`      | Data validation & serialization    |
| `python-dotenv` | Environment configuration          |
| `requests`      | HTTP client (for future image API) |

---

## 🚀 Development

### Run Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Run Tests

```bash
# Add pytest to requirements.txt, then:
pytest
```

### Interactive API Docs

```
http://localhost:8000/docs
```

---

## 🧠 Future Roadmap

### Phase 1: Prompt History API ✅ (in progress)
- GET `/prompts` - List all stored prompts
- GET `/prompts/{id}` - Get specific prompt
- DELETE `/prompts/{id}` - Delete prompt
- Requires Supabase for persistence

### Phase 2: Advanced Prompt Features
- POST `/analyze` - Semantic similarity between prompts
- POST `/variations` - Generate 5 variations of last prompt
- Implement vector embeddings with Supabase pgvector

### Phase 3: Batch Operations
- POST `/batch/generate` - Multiple images in one call
- Job queue with status tracking
- Webhooks for completion notifications

### Phase 4: Frontend
- Streamlit UI for quick prototyping
- React SPA for production (WebSocket for real-time)
- Image gallery with prompt history

### Phase 5: Advanced
- User authentication & prompt marketplace
- LoRA fine-tuning endpoint
- Custom model training on image/prompt pairs
- Multi-provider support (OpenAI, Anthropic, local Ollama)

---

## 📝 Notes

- This is a **prototype architecture** focusing on workflow and modularity
- Designed to scale from local development to production AI pipelines
- Each component can be replaced/upgraded independently
- No vendor lock-in: abstracted behind simple module interfaces
