# FactFinder

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Node](https://img.shields.io/badge/Node-20%2B-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)](https://langchain-ai.github.io/langgraph/)

An automated fact-checking engine built with **LangGraph** and **Next.js**. The system decomposes input statements into atomic claims, gathers real-time search evidence across the web, verifies claim validity, and generates structured truthfulness reports.

---

## Key Features

- **Atomic Claim Extraction**: Automatically extracts independent, testable claims from complex text and discourse while resolving coreferences and context.
- **Evidence-Based Verification**: Queries search engines to locate authoritative corroborating and refuting sources.
- **Multi-Status Classification**: Labels individual claims as **Supported**, **Refuted**, or **Insufficient Evidence** with confidence justifications.
- **Interactive Web Interface**: Real-time progress monitoring and detailed claim breakdown visualizations.
- **Modular Monorepo Architecture**: Clean separation between AI agent pipelines and the frontend interface.

---

## System Architecture

```mermaid
flowchart LR
    A[Input Text] --> B[Claim Extractor]
    B --> C[Claim Verifier]
    C --> D[Evidence Search]
    D --> C
    C --> E[Report Generator]
    E --> F[Verification Report]
```

- **`apps/agent`**: Python backend powered by LangGraph, coordinating extraction, search retrieval, and claim classification workflows.
- **`apps/web`**: Modern Next.js application providing the web dashboard, user authentication, and report history.

---

## Getting Started

### Prerequisites

- **Node.js**: v20 or higher
- **pnpm**: v10+ (`npm install -g pnpm@10.11.0`)
- **Python**: 3.11
- **Poetry**: Dependency manager for Python (`pip install poetry`)
- **LangGraph CLI**: `pip install "langgraph-cli[inmem]"`

### 1. Clone the Repository

```bash
git clone https://github.com/DEADEND-47/ClaimAI.git
cd ClaimAI
```

### 2. Configure Environment Variables

Create `.env` files for both the agent and the web application:

#### Agent Configuration (`apps/agent/.env`)
```env
OPENAI_API_KEY=your_openai_api_key
TINYFISH_API_KEY=your_tinyfish_api_key
SEARCH_PROVIDER=tinyfish
TAVILY_API_KEY=your_tavily_api_key
```

#### Web Configuration (`apps/web/.env`)
```env
OPENAI_API_KEY=your_openai_api_key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
DATABASE_URL=postgres://postgres:postgres@localhost:5432/main
UPSTASH_REDIS_REST_URL=http://localhost:8080
UPSTASH_REDIS_REST_TOKEN=local_dev_token
```

### 3. Install Dependencies

Install all dependencies across the monorepo:

```bash
pnpm setup:dev
```

### 4. Run the Application

Start both the backend agent server and the frontend web app simultaneously:

```bash
pnpm dev
```

Alternatively, you can run components individually:

- **Agent Server**: `pnpm backend:dev` (runs on `http://localhost:2024`)
- **Web Frontend**: `pnpm frontend:dev` (runs on `http://localhost:3000`)

---

## Project Structure

```
FactFinder/
├── apps/
│   ├── agent/                # LangGraph agents & verification pipeline
│   │   ├── claim_extractor/  # Claim extraction node
│   │   ├── claim_verifier/   # Evidence search & verification node
│   │   ├── fact_checker/     # Orchestrator & report generator
│   │   └── utils/            # Helper utilities
│   ├── web/                  # Next.js web application
│   │   ├── public/           # Static assets
│   │   └── src/              # UI components, pages & API routes
│   └── extension/            # Browser extension (optional)
├── packages/                 # Shared configurations & utilities
├── turbo.json                # Turborepo build pipeline
└── package.json              # Monorepo workspaces definition
```

---

## 🙏 Acknowledgements

This project builds upon and draws inspiration from the following work:

* Dasha Metropolitansky & Jonathan Larson from Microsoft Research - their [Claimify](https://arxiv.org/abs/2502.10309) methodology for claim extraction and disambiguation.
* Jerry Wei and the Google DeepMind team - the [SAFE](https://arxiv.org/abs/2403.18802) paper for multi-step search-augmented verification.
* The LangChain team - LangGraph for workflow orchestration.
* OpenAI - for the reasoning models powering understanding and verification.
* TinyFish & Tavily AI - for search and live web intelligence.

---

## 📞 Contact & Support

- **Author**: Kunal Lamba ([@DEADEND-47](https://github.com/DEADEND-47))
- **Issues**: Please use the [GitHub Issue Tracker](https://github.com/DEADEND-47/ClaimAI/issues) to report bugs or request features
- **Email**: [kunallamba47@gmail.com](mailto:kunallamba47@gmail.com)

---

## License

This project is licensed under the [MIT License](./LICENSE).
