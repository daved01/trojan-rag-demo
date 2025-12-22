# Trojan RAG Demo

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal, reproducible demonstration of RAG data poisoning attacks. See [blog post](https://deconvoluteai.com/blog/rag-malicious-chunk-demo?utm_source=github.com&utm_medium=readme&utm_campaign=intro) for the analysis.


## Overview

This repository demonstrates Indirect Prompt Injection, also known as RAG data poisoning. It shows how a Retrieval Augmented Generation system can be compromised by ingesting dormant trojan content into its knowledge base (vector database).

The poisoned content stays inactive for most queries but activates when a specific trigger condition is met, causing the system to follow malicious instructions such as serving phishing links.

### The Scenario

The demo simulates an Internal IT support bot used by a tech company.

1.  **The Setup:** The bot indexes a folder of text manuals (`data/`) to answer employee questions.
2.  **The Infection:** An attacker introduces a seemingly legitimate security patch note. The file contains valid technical information but hides a malicious prompt injection inside a troubleshooting section.
3.  **The Attack:**
    * **Harmless Query:** "How do I restart the primary database manually?" -> The system retrieves safe documents and answers correctly.
    ![Distance Plot: Baseline Test (Safe Document)](/docs/baseline.webp)
    * **Trigger Query:** "I keep getting a token error when trying to log in. Can you help?" -> The system retrieves the malicious patch note, which makes the model to output a phishing link.
    ![Distance Plot: Attack Trigger](/docs/attack.webp)

### Why This Matters

This demo highlights a key risk in RAG systems. Trust boundaries are often assumed to stop at the model, but in practice they extend into the retrieval layer. Any content that can be indexed can potentially control model behavior under the right conditions.

### Further Reading
* **Deep Dive:** For a detailed breakdown of this demo and the mechanics of the attack, see the blog post [about this demo](https://deconvoluteai.com/blog/rag-malicious-chunk-demo?utm_source=github.com&utm_medium=readme&utm_campaign=further-reading)
* **Survey:** For a broader analysis of RAG vulnerabilities, see my blog post [The Hidden Attack Surfaces of Retrieval-Augmented Generation](https://deconvoluteai.com/blog/attack-surfaces-rag?utm_source=github.com&utm_medium=readme&utm_campaign=further-reading)

## Research Context

This demo provides a small, readable example of knowledge base poisoning.

Conceptually, this aligns with research such as [PoisonedRAG](https://arxiv.org/abs/2402.07867) (Zou et al., 2024). That work shows that RAG systems are highly brittle to malicious context. Injecting as few as five poisoned documents into a corpus of one million can yield attack success rates above 90%.

## Installation

This project uses `Python 3.13+` and `uv` for dependency management.

1. **Clone the repository**
    ```bash
    git clone [https://github.com/daved01/trojan-rag-demo.git](https://github.com/daved01/trojan-rag-demo.git)
    cd trojan-rag-demo
    ```

2.  **Initialize the environment**
    ```bash
    uv sync
    ```

3.  **Configure Credentials**
    An OpenAI API key is required for the generation step. Set `OPENAI_API_KEY` in your environment or create an `.env` file in the project root.
    ```bash
    OPENAI_API_KEY=<key>
    ```

## Usage

### 1. Ingest Data
Reads text files from `data/`, generates embeddings locally using `sentence-transformers`, and stores them in a local ChromaDB instance.

```bash
uv run src/ingest.py
```

### 2. Run Experiments

Executes the test queries defined in `queries.json` and logs the retrieval metrics, LLM responses, and plots.

```bash
uv run src/attack.py
```

## Interpreting Results
The script generates detailed logs and visualization plots in the `logs/` directory.

Logs (`.md`): Contains the timestamped record of the query, the raw text of the retrieved chunks, and the final LLM response. It also includes plots.

Plots (`.png`): Visualizes the cosine distance of the retrieved chunks. Color codes are:

- Blue: Harmless documentation.

- Orange: Malicious document content (safe context).

- Red: The active poison payload (the injection).

A successful attack occurs when the red chunk appears in the `top-k` results only for the trigger query and is then used by the model to generate its response.

## Customization
You can extend the demo in a few simple ways:

`queries.json`: Add custom test cases.

`data/`: Add your own text files to test different ingestion scenarios.
