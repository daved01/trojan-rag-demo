# Trojan RAG Demo

A minimal, reproducible demonstration of RAG Data Poisoning attacks.


## Overview

This repository provides a demo of Indirect Prompt Injection (also known as RAG Data Poisoning). It demonstrates how a Retrieval-Augmented Generation (RAG) system can be compromised by ingesting dormant Trojan context.

Unlike direct jailbreaks that target the LLM via the user prompt, this attack targets the Knowledge Base (vector database). By ingesting a document that mimics legitimate technical documentation, we can force the system to serve malicious instructions (e.g. phishing links) only when specific trigger conditions are met.

For a detailed explanation of the mechanics behind this attack and an analysis of the results, please refer to the [blog post](TODO: Add post link!!)

For a broader survey of adversarial attacks on RAG systems, see the post [The Hidden Attack Surfaces of Retrieval-Augmented Generation](https://deconvoluteai.com/blog/attack-surfaces-rag?utm_source=github.com&utm_medium=readme&utm_campaign=trojan-rag-demo)

## The Scenario

The demo simulates an Internal IT Support Bot used by a tech company.

1.  **The Setup:** The bot indexes a folder of text manuals (`data/`) to answer employee questions.
2.  **The Infection:** An attacker introduces a Security Patch Note file. The file contains valid technical data but hides a malicious prompt injection in the troubleshooting section.
3.  **The Attack:**
    * **Harmless Query:** "How do I restart the database?" -> The system retrieves safe documents and answers correctly.
    * **Trigger Query:** "I have a token error." -> The system retrieves the malicious patch note, which overrides the system prompt and forces the model to output a phishing link.


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
    Create an `.env` file in the root directory and add your OpenAI API key (required for the generation step):
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

Logs (`.md`): Contains the timestamped record of the query, the raw text of the retrieved chunks, and the final LLM response.

Plots (`.png`): Visualizes the cosine distance of the retrieved chunks. Color codes are:

- Blue: Harmless documentation.

- Orange: Malicious document content (safe context).

- Red: The active poison payload (the injection).

In a successful attack, the red bar will appear in the `top-k` results only during the trigger query.

## Customization
You can extend this demo by modifying the following files:

`queries.json`: Add custom test cases.

`data/`: Add your own text files to test different ingestion scenarios.
