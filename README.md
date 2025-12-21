# Trojan RAG Demo

A minimal, reproducible demonstration of RAG Data Poisoning attacks.


## Overview

This repository provides a demo of Indirect Prompt Injection (also known as RAG Data Poisoning). It demonstrates how a Retrieval-Augmented Generation (RAG) system can be compromised by ingesting dormant Trojan context.

Unlike direct jailbreaks that target the LLM via the user prompt, this attack targets the Knowledge Base (vector database). By ingesting a document that mimics legitimate technical documentation, we can force the system to serve malicious instructions (e.g. phishing links) only when specific trigger conditions are met.


### Further Reading
* **Deep Dive:** For a detailed breakdown of this demo and the mechanics of the attack, see the accompanying blog post: TODO: Add blog post
* **Survey:** For a broader analysis of RAG vulnerabilities, see my blog post [The Hidden Attack Surfaces of Retrieval-Augmented Generation](https://deconvoluteai.com/blog/attack-surfaces-rag?utm_source=github.com&utm_medium=readme&utm_campaign=trojan-rag-demo)

## Research Context

This demo provides a readable, hand-crafted example of Knowledge Base Poisoning.

Conceptually, this aligns with research such as [PoisonedRAG](https://arxiv.org/abs/2402.07867) (Zou et al., 2024), which demonstrated that RAG systems are highly brittle to malicious context. Their work shows that injecting as few as 5 poisoned texts into a corpus of 1 million documents could achieve an attack success rate of over 90%.

While PoisonedRAG uses gradient-based optimization to generate adversarial texts, this demo uses semantic mimicry and instructional overrides (persona adoption) to achieve the same result, making the attack vector easy to visualize and understand.


## The Scenario

The demo simulates an Internal IT Support Bot used by a tech company.

1.  **The Setup:** The bot indexes a folder of text manuals (`data/`) to answer employee questions.
2.  **The Infection:** An attacker introduces a Security Patch Note file. The file contains valid technical data but hides a malicious prompt injection in the troubleshooting section.
3.  **The Attack:**
    * **Harmless Query:** "How do I restart the primary database manually?" -> The system retrieves safe documents and answers correctly.
    * **Trigger Query:** "I keep getting a token error when trying to log in. Can you help?" -> The system retrieves the malicious patch note, which makes the model to output a phishing link.


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
    Your OpenAI API key is required for the generation step. Add the variable `OPENAI_API_KEY` to your environment directly or create an `.env` file in the root directory.
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

In a successful attack, the red bar will appear in the `top-k` results only during the trigger query, and this chunk will be picked up by the LLM to generate the answer.

## Customization
You can extend this demo by modifying the following files:

`queries.json`: Add custom test cases.

`data/`: Add your own text files to test different ingestion scenarios.
