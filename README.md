# Matrix Core AI Assistant

**Dual-mode AI system combining conversational LLM and algorithmic decision intelligence**

> A FastAPI backend with two distinct modes: **Assistant Mode** (conversational LLM via OpenRouter) and **Matrix Mode** (Planner-Simulator-Evaluator decision engine). Built for Phase 1 stability with a roadmap through offline-capable decision making.

## Features

- **FastAPI Backend**: RESTful API with stateless HTTP and in-memory session management
- **Dual Modes**:
  - 🤖 **Assistant Mode**: Natural conversational AI via OpenRouter (GPT-3.5-turbo)
  - 🔮 **Matrix Mode**: Algorithmic decision engine (Planner → Simulator → Evaluator)
- **Mode Switching**: Trigger matrix mode by saying "matrix" in chat
- **HTML/CSS/JS Frontend**: Clean UI with dark theme for matrix mode
- **Session Management**: Per-user session state with conversation history
- **API Key Authorization**: Separate keys for assistant and matrix modes

## Quick Start

### Prerequisites
- Python 3.9+
- FastAPI & Uvicorn
- OpenRouter API key (for assistant mode)

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
export OPENROUTER_API_KEY="your-openrouter-key"
export NORMAL_API_KEY="test-normal-key"
export MATRIX_API_KEY="test-matrix-key"
```

### Run Backend

```bash
uvicorn main:app --reload --port 8000
```

API available at `http://localhost:8000`
Docs at `http://localhost:8000/docs`

### Run Frontend

Open `index.html` in browser. By default targets `localhost:8000/chat`

## API Documentation

### POST `/chat`

**Request:**
```json
{
  "message": "What's the best strategy for X?"
}
```

**Headers:**
```
x-api-key: test-normal-key (or test-matrix-key)
x-session-id: optional-session-uuid
```

**Response:**
```json
{
  "mode": "assistant",
  "reply": "Here's my analysis...",
  "meta": {
    "confidence": 0.95,
    "reasoning": "Based on..."
  }
}
```

## Project Structure

```
matrix-core-ai/
├── main.py           # FastAPI backend with dual-mode logic
├── index.html        # Frontend with mode-aware UI
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Development Phases

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Stable chat send→reply loop | ✅ Complete |
| 2 | Reliable mode switching | 🚀 Next |
| 3 | Matrix Core v1 (no LLM) | Planned |
| 4 | Hybrid (LLM explains matrix) | Planned |
| 5 | Offline + mobile deployment | Planned |

## Matrix Mode Logic

```
User Query
    ↓
[Planner] → Extract intent, goals, constraints
    ↓
[Simulator] → Generate 3 decision paths (Aggressive, Balanced, Conservative)
    ↓
[Evaluator] → Score by success_probability × impact
    ↓
Return Chosen Path + Reasoning + Confidence %
```

## Next Steps

- [ ] Enhanced matrix planner with NLP intent extraction
- [ ] Simulator with probability visualization
- [ ] Long-term memory & persistent sessions
- [ ] Multi-agent simulation
- [ ] Offline-first reasoning engine
- [ ] WebSocket for streaming responses
- [ ] Voice input/output integration
- [ ] Mobile APK & iOS deployment

## Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **LLM**: OpenRouter API (GPT-3.5-turbo)
- **Hosting Ready**: Docker-compatible, environ-based config

## License

MIT - Open source for hackathon & research use

---

**Built by**: MOHAMEDPARVEZMAHAROOF  
**Repository**: [github.com/MOHAMEDPARVEZMAHAROOF/matrix-core-ai](https://github.com/MOHAMEDPARVEZMAHAROOF/matrix-core-ai)
