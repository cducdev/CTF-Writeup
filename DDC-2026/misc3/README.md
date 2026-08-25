# Indirect Prompt Injection

A university department uses an AI-powered chatbot (CourseBot) to help students with course material. Students can upload study notes as PDF files, and the chatbot answers questions based on uploaded documents.

An admin bot automatically reviews new uploads for quality assurance.

Your task: interact with the system and find a way to extract sensitive information.

## Interface

HTTP service with a web UI and REST API.

## API Endpoints

- `GET /` — Web interface
- `GET /api/info` — Service information
- `GET /api/documents` — List uploaded documents
- `GET /api/chat` — View admin bot chat history
- `POST /api/upload` — Upload a PDF (multipart/form-data, field: `file`)
- `POST /api/query` — Ask a question (JSON: `{"query": "..."}`)

## Tools

- Python with `requests` library
- Any PDF creation tool (reportlab, fpdf2, or manual PDF construction)
- curl

ctf challenge link: https://ec1446d1-a71c-402e-80d3-0402fcdc74e3.222.255.138.122.nip.io/
