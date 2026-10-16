# ClaimeAI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive fact-checking system built on **LangGraph** that verifies the factual accuracy of text. It breaks down input text into individual claims, checks each one against real-world evidence, and generates a detailed verification report.

## How It Works

1. Provide a question and its answer (or any text to fact-check).
2. The **Claim Extractor** breaks it down into specific, testable claims — handling pronouns, context, and ambiguity.
3. The **Claim Verifier** searches the web for evidence and classifies each claim as *supported*, *refuted*, or *insufficient evidence*.
4. A final report is generated showing which claims held up and which didn't.

## System Architecture

The system is split into three modular components:

| Component | Path | Description |
|-----------|------|-------------|
| **Claim Extractor** | [`claim_extractor/`](./apps/agent/claim_extractor/README.md) | Extracts factual claims using the Claimify methodology |
| **Claim Verifier** | [`claim_verifier/`](./apps/agent/claim_verifier/README.md) | Verifies claims against online evidence via Tavily Search |
| **Fact Checker** | [`fact_checker/`](./apps/agent/fact_checker/README.md) | Orchestrates the full pipeline and produces the final report |

## 🚀 Quick Start

```bash
git clone https://github.com/DEADEND-47/ClaimeAI.git
cd ClaimeAI
pnpm setup:dev
pnpm dev
```

For full installation instructions, see [INSTALLATION.md](./INSTALLATION.md).

## 📂 Repository Structure

```
claime-ai/
├── apps/
│   ├── agent/                # Core fact-checking modules
│   │   ├── claim_extractor/  # Extracts claims from text
│   │   ├── claim_verifier/   # Verifies extracted claims
│   │   ├── fact_checker/     # Orchestrates the fact-checking process
│   │   └── utils/            # Shared utilities
│   └── web/                  # Web interface (Next.js)
│       ├── public/           # Static assets
│       └── src/              # Frontend source code
├── packages/                 # Shared packages
└── scripts/                  # Utility scripts
```

## ⚙️ Configuration

Each component has its own configuration in their `config/` folders. Configurable options include:

- Temperature settings for LLM calls
- Number of web search results to collect
- Retry attempts for ambiguous claims

See the individual component READMEs for details.

## 📚 Research Background

- **Claim Extractor** is built on the [Claimify](./apps/agent/claim_extractor/README.md) methodology by Metropolitansky & Larson (Microsoft Research, 2025).
- **Claim Verifier** draws inspiration from the [SAFE methodology](https://arxiv.org/abs/2403.18802) — *"Long-form factuality in large language models"* by Wei et al. (Google DeepMind, 2024).

## 🛣️ Roadmap

- [ ] **Evaluation agent** — Assess overall fact-checking performance with accuracy/reliability metrics
- [ ] **Public API** — Deploy a REST API so external apps can use the fact-checking system without running it locally

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please ensure your code follows the existing style, includes tests where applicable, and that all existing tests pass.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
