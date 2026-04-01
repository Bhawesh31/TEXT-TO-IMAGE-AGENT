# 🧠 Project: Autonomous Text-to-Image Generation Agent

## 🎯 Objective

Build an AI workflow where an agent:

1. Takes a basic user concept (e.g., "car")
2. Enhances it into a detailed prompt
3. Generates an image
4. Supports iterative conversational editing

---

## 🏗️ Architecture Overview

User Input → FastAPI Backend → LLM Agent (Prompt Enhancer) → Image Generator → Vector Memory

---

## 🧩 Components

### 1. LLM Agent (Art Director)

* Enhances user input into detailed prompts
* Adds:

  * Style
  * Lighting
  * Environment
  * Camera angle

Example:
Input: "car"
Output: "A futuristic red sports car, cinematic lighting, ultra-detailed, 4K, neon reflections"

---

### 2. Image Generator

* Takes enhanced prompt
* Returns image URL
* Currently uses placeholder (dummy image API)
* Designed to integrate with Stable Diffusion or external APIs

---

### 3. Memory (Vector DB Simulation)

* Stores previous prompts
* Enables editing like:

  * "make it sunset lighting"
  * "same style as previous"

Implementation:

* Lightweight in-memory storage (list-based)
* Replaceable with ChromaDB / FAISS in production

---

### 4. Editing System

* Uses last stored prompt
* Appends user modifications
* Regenerates image

---

## ⚙️ Backend Requirements

* Framework: FastAPI
* Endpoints:

  * POST /generate → create image from idea
  * POST /edit → modify previous image

---

## 🧱 Code Structure

backend/

* app.py → main API
* llm.py → prompt enhancement logic
* image.py → image generation
* vector_db.py → memory handling

---

## 🐳 Docker Requirements

* Use Python 3.10
* Install dependencies from requirements.txt
* Run FastAPI using Uvicorn
* Expose port 8000

---

## 📦 Dependencies

* fastapi
* uvicorn
* requests
* python-dotenv

---

## 🎨 Fine-Tuning (LoRA)

Provide a notebook that includes:

* Dataset description
* Training configuration:

  * epochs
  * batch size
  * learning rate
* Simulated or real loss curve

No need to include heavy model files.

---

## 📘 README Requirements

Include:

1. Setup instructions (docker-compose up)
2. Architecture diagram (text-based)
3. Design decisions:

   * Why FastAPI
   * Why lightweight memory instead of full DB
4. Trade-offs:

   * No GPU → used placeholder image generator
   * API fallback for reliability

---

## 🎯 Goals for Copilot

When generating code:

* Keep modules separate (llm, image, vector_db)
* Write clean, readable Python
* Add comments explaining logic
* Ensure API endpoints work correctly
* Avoid unnecessary complexity
* Prefer simple working solutions over heavy dependencies

---

## 🚀 Future Improvements

* Replace placeholder image generator with Stable Diffusion
* Integrate real vector DB (Chroma / FAISS)
* Add real LLM API (Bytez / OpenAI)
* Add frontend (Streamlit / React)

---

## 🧠 Notes

* This is a prototype focused on architecture and workflow
* System is designed to scale to production-level AI pipelines
