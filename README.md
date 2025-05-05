# AI-Enhanced Distributed Web Crawler

A Java + Python hybrid system that supports concurrent task scheduling, intelligent web crawling, and AI-powered text analysis.

## Project Overview

This project is a hybrid full-stack system that uses **Java** for high-performance task orchestration and **Python** for powerful web scraping and NLP. Users can submit a URL or keyword, and the system will:
1. Crawl relevant web content.
2. Analyze text sentiment, extract keywords, and generate summaries.
3. Store and display the results through APIs and an optional UI.

> Although it's designed to run on a single machine, it simulates a distributed architecture using multi-process modular services communicating via HTTP or message queues.

## System Architecture

```
[ User / Frontend UI ]
         ↓
  [ Java REST API ]
         ↓
[ Task Manager / Thread Pool ]
         ↓                 ↘
[ Python Crawler Service ]   [ Python NLP Service ]
         ↓                      ↓
     Extracted Text        Analyzed JSON
         ↘                      ↙
             [ Relational/NoSQL Database ]
```

## Project Structure

```
ai-crawler-project/
├── java-backend/           # Java: task manager, API, DB, async controller
├── python-crawler/         # Python: fast crawler service
├── python-nlp/             # Python: NLP analysis (keywords, sentiment, summary)
├── shared/                 # Common schemas / test input / docs
├── docker-compose.yml      # Service orchestration
└── README.md
```

## Technologies

| Module | Tech Stack |
|--------|------------|
| **Backend (API)** | Java, Spring Boot, REST API, JPA, CompletableFuture |
| **Task Scheduling** | Java ExecutorService, async HTTP clients |
| **Web Crawling** | Python (requests, BeautifulSoup, Flask/FastAPI) |
| **Text Analysis** | Python (spaCy, transformers, VADER) |
| **Database** | MySQL (via Spring Data JPA) or MongoDB |
| **Frontend (optional)** | HTML/JS or Vue.js (future integration) |
| **Containerization** | Docker + Docker Compose |

## Getting Started

### 1. Prerequisites

- JDK 17+
- Python 3.10+
- Docker & Docker Compose

### 2. Clone & Build

```bash
git clone https://github.com/yourname/ai-crawler-project.git
cd ai-crawler-project
```

### 3. Run via Docker Compose

```bash
docker-compose up --build
```

Services exposed:
- Java Backend: http://localhost:8080
- Python Crawler: http://localhost:5001
- Python NLP: http://localhost:5002
- DB: port 3306

## API Specification (Draft)

### `POST /task`
Submit a crawl task.

```json
{
  "type": "url",            // or "keyword"
  "payload": "https://example.com"
}
```

### `GET /task/{id}`
Check task status and result.

### `POST /crawl`
Internal (Python crawler): Get text from a webpage

```json
{ "url": "https://example.com" }
```

### `POST /analyze`
Internal (Python NLP): Analyze raw text

```json
{ "text": "The quick brown fox jumps over the lazy dog." }
```

## Development Plan

| Week | Task |
|------|------|
| 1 | Define interfaces, initialize Java & Python projects |
| 2 | Java: build API & thread pool; Python: setup services |
| 3 | Implement crawler and NLP modules |
| 4 | Integrate end-to-end (Java → Crawler → NLP → DB) |
| 5 | Add UI + result visualization |
| 6 | Polish, test, write documentation, create demo |

## Contributors

- Lyuyongkang Yuan
- Junwei Yan

## License

MIT License (or your choice)
"# News-and-Opinion-Analysis" 
