# ATG Task 2 — Multi-Agent Debate DAG (LangGraph-style)

## Overview
Small CLI program that simulates an 8-round debate between two personas (Scientist vs Philosopher). Memory is updated and passed selectively; a judge summarizes and declares a winner. All messages, states, and decisions are logged.

## Setup
```bash
python -m venv venv
source venv/bin/activate      # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Run
```bash
python run_debate.py
```

Follow the CLI prompt to enter a topic.

## Deliverables produced by the program
- `logs/debate.log` (full textual log)
- `logs/debate_state.json` (structured state and memory)
- `diagrams/debate_dag.png` (generated DAG)

## Notes
- The agent implementations are deterministic template-based. You can swap them with actual LLM calls in `nodes.py`.
- If you want a LangGraph-native implementation, tell me and I will convert the node definitions.
