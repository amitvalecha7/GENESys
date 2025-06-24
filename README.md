# GENESys: Intelligent Orchestrator for AI-Agent Ecosystems

Welcome to **GENESys**, a chatbot-driven orchestrator that automates discovery, provisioning, and documentation of your AI/LLM services and infrastructure.

---

## 🚀 Repository Structure

├── backend/
│ ├── genesys-backend/ # Original FastAPI UI-serving backend
│ └── orchestrator_api/ # Orchestrator service
│ ├── app/
│ │ ├── api/ # Chat & workflow router endpoints
│ │ ├── models/ # Pydantic schemas
│ │ ├── services/ # Agent logic (discovery, provisioning)
│ │ └── utils/ # SSH helper, logger
│ ├── tests/ # pytest smoke tests
│ ├── Dockerfile # Orchestrator container definition
│ └── requirements.txt # Python dependencies
├── frontend/ # Streamlit-based chatbot UI
├── docker-compose.yml # Multi-service orchestration
├── docs/ # Operational manuals & templates
└── README.md # This document

yaml
Copy
Edit

---

## 🔧 Prerequisites

- Docker & Docker Compose installed on your nodes
- Python 3.12 (for local development)
- SSH key access to your target servers

---

## 📦 Getting Started

### 1. Clone the Repo
```bash
git clone git@github.com:amitvalecha7/GENESys.git
git checkout main
2. Launch All Services
bash
Copy
Edit
cd GENESys
docker-compose up -d --build
UI (Streamlit + FastAPI): https://console.dhii.ai or http://localhost:3012

Orchestrator API: http://localhost:8010

n8n: http://localhost:5678

3. Test Orchestrator Endpoints
bash
Copy
Edit
# Health check
curl http://localhost:8010/chat/health

# Echo chat
curl -X POST http://localhost:8010/chat/message \
  -H 'Content-Type: application/json' \
  -d '{"message":"hello"}'

# Node discovery
curl -X POST http://localhost:8010/workflows/discover \
  -H 'Content-Type: application/json' \
  -d '[{"host":"127.0.0.1","user":"root","key_path":"~/.ssh/id_rsa"}]'
📑 Operational Manual Template
See docs/manual_template.md for a starting point on documenting deployments, architecture, and runbooks.

🛠️ CI/CD Integration
A GitHub Actions workflow (.github/workflows/ci.yml) runs on every push:

Lint: flake8 checks

Test: pytest smoke tests

Docker Build: Builds the orchestrator image

Results are reported on each PR and main branch push.

📅 Roadmap
Phase	Status
Infra Groundwork	✅ Completed
Orchestrator SOW 1–4	✅ Completed
Day 5 (Agents)	✅ Completed
Day 6 (Dockerize)	✅ Completed
Day 7 (Docs & CI)	🔄 In Progress

For detailed dev instructions, check the docs/ folder or contact the GenAI team.
