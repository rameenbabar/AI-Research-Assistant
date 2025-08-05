# AI Research Assistant

## Overview

This project streamlines academic literature review by semantically retrieving AI/ML arXiv papers, answering researcher questions, extracting explicit scope & dataset details, and auto-generating a narrated slide-video—all with open-source LLMs.

It demonstrates end-to-end Retrieval-Augmented Generation (RAG), hybrid dense + sparse vector search, prompt-driven information extraction, and lightweight multimedia production without closed APIs.

---

## Dataset

We index a focused slice of arXiv:

- **Domain:** Artificial Intelligence + Machine Learning

- **Storage:** Qdrant Cloud collection axRiv_research_papers

For quick tests, change `top_k_results` in `data_ingestion.ipynb` to a smaller number.

* **Source Link:** <https://arxiv.org/search/?query=artificial+intelligence+machine+learning&searchtype=all>

---

## Objective

**Build a research-assistant system that:**

- Discovers relevant papers via hybrid semantic search.

- Answers user questions strictly from retrieved context.

- Extracts future-research gaps from stated limitations.

- Lists literal dataset names used in a paper.

- Produces a narrated video summary of any indexed paper.

---

## Technologies Used

**Python** – core orchestration

**LangChain + LangGraph** – state-graph pipelines

**HuggingFace Embeddings (BAAI/bge-base-en-v1.5)** – dense vectors

**Qdrant/BM25** – sparse vectors

**Qdrant Vector DB** – hybrid retrieval

**Ollama (Mistral)** – open-source LLM

P**yMuPDF · OpenCV · MoviePy · gTTS** – PDF-to-video pipeline

---

## Workflow Overview

### 1. Paper Ingestion

- Fetch papers with `ArxivLoader`

- Split into semantic chunks via `SemanticChunker`

- Upsert dense + sparse vectors to Qdrant `(RetrievalMode.HYBRID)`

### 2. Paper Retrieval & Question Answering

- Query Optimisation Prompt condenses user input

- Top-k hybrid search returns context

- Mistral answers

### 3. Information Extraction

- Scope extractor maps limitations → future research gaps

- Dataset extractor outputs exact dataset names 

### 4. Video Generation

- Retrieve stored summary

- Rewrite to conversational script

- TTS → MP3

- Convert PDF pages → frames → stitch with audio → MP4

---

## How to run project

```bash
git clone https://github.com/yourusername/AI-Research-Assistant.git
cd AI-Research-Assistant
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Configuration

All sensitive credentials and configuration parameters are stored in a dedicated `configs.py`

#### configs.py Template

```bash
QDRANT_API_KEY = "your-qdrant-api-key"
QDRANT_URL = "https://your-qdrant-instance"
OLLAMA_URL = ""
```

---

## Deployment Notes

Works on local CPU; use GPU or server CPUs for lower latency.

Qdrant can be self-hosted via Docker or Qdrant Cloud.

Swap Ollama model `(gemma3, mistral)` to trade accuracy vs. speed.

**For scaling:** deploy ingestion on a Spark/Flink job, shard Qdrant, and front the pipelines with FastAPI.

---

