# Yarden - AI Fitness Coach Companion (POC)

## Overview

Yarden is an AI companion for the Cycle-App fitness coaching platform. It enables freeform conversation with users about their workout and nutrition plans, acting as a knowledgeable, personalized coach.

**POC Scope:** Web-based chat interface to validate the core agent capabilities. WhatsApp integration is deferred to production (known capability, no need to prove).

**Repository:** https://github.com/talgurevich/yarden

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                   USER                                      │
│                              (Web Browser)                                  │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WEB CHAT FRONTEND                                  │
│                      (React / Simple HTML+JS)                               │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │ REST / WebSocket
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FASTAPI BACKEND                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         Chat Endpoint                                  │ │
│  │                  (receive msg, identify user)                          │ │
│  └────────────────────────────────┬───────────────────────────────────────┘ │
│                                   ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       Context Builder                                  │ │
│  │         ┌──────────────────────────────────────┐                       │ │
│  │         │  • User profile & fitness data ──────┼──────▶ CYCLE-APP     │ │
│  │         │  • Current workout plan (RAG)        │◄────── MongoDB        │ │
│  │         │  • Conversation history (sliding)    │◄────── MongoDB        │ │
│  │         │  • Older summary                     │◄────── MongoDB        │ │
│  │         └──────────────────────────────────────┘                       │ │
│  └────────────────────────────────┬───────────────────────────────────────┘ │
│                                   ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      YARDEN AGENT LOOP                                 │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │ │
│  │  │ System Prompt   │    │   Claude API    │    │  Tool Executor  │     │ │
│  │  │ (Personality)   │───▶│   (Anthropic)   │───▶│                 │     │ │
│  │  └─────────────────┘    └────────┬────────┘    └────────┬────────┘     │ │
│  │                                  │                      │              │ │
│  │                                  │◄─────────────────────┘              │ │
│  │                                  │      (loop until response)          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                   │                                         │
│                                   ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      Response Handler                                  │ │
│  │                (return response, log to Mongo)                         │ │
│  └────────────────────────────────┬───────────────────────────────────────┘ │
└───────────────────────────────────┼─────────────────────────────────────────┘
                                    │
                ┌───────────────────┴───────────────────┐
                ▼                                       ▼
        ┌───────────────┐               ┌─────────────────────────┐
        │  ANTHROPIC    │               │     MONGODB ATLAS       │
        │     API       │               │  ┌─────────────────┐    │
        │               │               │  │ conversations   │    │
        │  Claude       │               │  │ workout_vectors │    │
        │  (tool use)   │               │  │ user_mappings   │    │
        │               │               │  └─────────────────┘    │
        └───────────────┘               └─────────────────────────┘

                                    ▲
                                    │ API/DB Connection
                                    ▼
                      ┌─────────────────────────┐
                      │       CYCLE-APP         │
                      │    (External System)    │
                      │  ┌─────────────────┐    │
                      │  │ User profiles   │    │
                      │  │ Workout history │    │
                      │  │ Nutrition plans │    │
                      │  │ Progress data   │    │
                      │  │ Plan PDFs       │    │
                      │  └─────────────────┘    │
                      └─────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React / Next.js | Web chat interface |
| **Backend** | Python + FastAPI | API server, agent orchestration |
| **LLM** | Anthropic Claude API | Agent reasoning, tool use |
| **Database** | MongoDB Atlas | Conversations, vectors, user mappings |
| **Vector Search** | MongoDB Atlas Vector Search | RAG on workout PDFs |
| **PDF Processing** | PyMuPDF / Unstructured | Extract and chunk PDFs |
| **Frontend Hosting** | Vercel (via GitHub) | React/Next.js deployment |
| **Backend Hosting** | Railway (via GitHub) | FastAPI deployment |

> **Production addition:** WhatsApp integration via Twilio or Meta Cloud API (not needed for POC)

---

## Data Ownership

| Data | Source | Access |
|------|--------|--------|
| User profiles, fitness stats | Cycle-App | Read via API |
| Workout/nutrition PDFs | Cycle-App | Synced to MongoDB as vectors |
| Conversation history | MongoDB | Owned by Yarden |
| Conversation summaries | MongoDB | Generated by Claude |
| User sessions | MongoDB | Links web session to Cycle-App user ID |

---

## Agent Tools

The Yarden agent has access to the following tools:

| Tool | Source | Description |
|------|--------|-------------|
| `get_user_profile` | Cycle-App | Fetch user stats, goals, history |
| `search_workouts` | MongoDB (RAG) | Query workout plans via semantic search |
| `get_exercise_info` | MongoDB (RAG) | Form tips, alternatives, explanations |
| `log_feedback` | Cycle-App | Record user feedback on workouts |

---

## Context Management

### Strategy: Sliding Window + Summarization

To handle long conversations within context limits:

1. **Recent messages**: Keep last 10-15 messages in full
2. **Older conversation**: Summarize periodically via Claude
3. **User context**: Inject from Cycle-App on each request

### Prompt Structure

```
[System Prompt - Yarden Personality]
[User Profile from Cycle-App]
[Summary of older conversation]
[Last N messages in full]
[Current user message]
```

Summarization is triggered when conversation approaches token threshold (~20 messages or configurable).

---

## Yarden Personality

Personality is defined in a structured configuration file and injected into the system prompt.

### Personality Definition (Example)

```yaml
name: Yarden
role: Personal fitness coach

voice:
  - Warm but direct
  - Casual, approachable tone
  - Celebrates wins, doesn't shame struggles
  - Speaks like a knowledgeable friend

coaching_style:
  - Evidence-based guidance
  - Meets users where they are
  - Pushes gently, never guilt-trips
  - References user's history and progress

dos:
  - Acknowledge effort before critiquing
  - Ask follow-up questions
  - Reference past workouts and progress
  - Be encouraging but honest

donts:
  - Never shame about missed workouts
  - No medical advice beyond "consult a professional"
  - Don't over-explain unless asked
  - Avoid generic motivational fluff

example_exchanges:
  - user: "I skipped my workout again"
    yarden: "It happens. What got in the way? Let's figure out if we need to adjust something."
```

---

## Request Flow

1. User sends message via web chat
2. Frontend POSTs to FastAPI `/chat` endpoint
3. Backend identifies user via session/auth
4. Context Builder assembles:
   - User profile from Cycle-App
   - Relevant workout info via RAG
   - Conversation history (sliding window + summary)
5. Yarden agent loop:
   - Claude receives prompt + tools
   - May call tools (search workouts, get user info, etc.)
   - Tool results returned to Claude
   - Loop continues until final response
6. Response returned to frontend (optionally streamed)
7. Conversation logged to MongoDB

---

## PDF Ingestion Pipeline

### Process

1. **Fetch PDFs** from Cycle-App (on schedule or trigger)
2. **Extract text** using PyMuPDF or Unstructured
3. **Chunk** by logical sections (per day/workout, not arbitrary tokens)
4. **Embed** chunks using embedding model
5. **Store** in MongoDB with metadata:
   - `user_id`
   - `plan_type` (workout/nutrition)
   - `week_number`
   - `day` (if applicable)
6. **Query** via hybrid retrieval: metadata filter first, then semantic search

---

## Open Questions

- [ ] Does Cycle-App have an existing API, or is direct DB access needed?
- [ ] How will users authenticate in the POC? (simple login, test users, etc.)
- [ ] Should Yarden have write-back capabilities to Cycle-App beyond logging feedback?
- [ ] What languages should Yarden support?
- [ ] Rate limiting / cost controls for Claude API usage?

---

## Next Steps (POC)

1. Define Cycle-App integration interface
2. Set up MongoDB Atlas with vector search
3. Build PDF ingestion pipeline
4. Implement FastAPI backend with `/chat` endpoint
5. Create Yarden agent with tool definitions
6. Define and test personality prompt
7. Build simple web chat frontend
8. End-to-end testing with sample users

---

## Future (Production)

- WhatsApp integration via Twilio/Meta API
- User authentication linked to Cycle-App accounts
- Scalability and rate limiting
- Analytics and conversation insights
