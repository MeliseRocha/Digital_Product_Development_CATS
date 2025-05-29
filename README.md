# AI-Powered Medical History Generator

An intelligent tool that collects and organizes structured **medical histories** through conversational interactions. This project uses **Rasa** for handling natural dialogue and **LLaMA-based models** to refine and enrich clinical data. 

---

## Features

- **Conversational Medical History Collection**  
  Patients interact via chat or voice to provide symptoms and background.

- **LLM-Powered Data Enrichment**  
  Fine-tuned LLaMA models clean, complete, and organize medical information.

- **Structured Output with ICD-10 Mapping**  
  Outputs can include structured SOAP-style summaries and coded data.

- **EHR-Ready Format**  
  Designed for seamless integration with Electronic Health Record systems.

---

## Architecture Overview

### Frontend
- `HTML`, `CSS`, `JavaScript`
- Collects user input and interfaces with the backend via REST

### Conversational Engine
- `Rasa Open Source`
- Handles dialog flow, entity extraction, slot filling

### Backend
- `Flask-RESTful` (Python)
- Connects Rasa, frontend, and LLaMA-powered processing

### AI Engine
- Fine-tuned **LLaMA** model for:
  - Data normalization and summarization
  - ICD-10 code suggestion
  - Follow-up question generation

---

## Tech Stack

| Component     | Tech                      |
|---------------|---------------------------|
| Conversational AI | Rasa (NLU + Core)         |
| NLP Model     | Fine-tuned LLaMA           |
| Backend API   | Flask-RESTful              |
| Frontend      | HTML, CSS, JavaScript      |
| Deployment    | Docker + Nginx (optional)  |


