# News NLP Analyzer

A distributed system for keyword-based news crawling and NLP analysis. It combines a Spring Boot backend for task dispatching, Python services for crawling and NLP processing, Redis for task queueing, and MySQL for result storage. The entire system can be launched via Docker Compose.

## Features

- **Keyword-driven news crawling** via Python + requests + newspaper3k  
- **Task dispatching & coordination** via Java Spring Boot backend  
- **Asynchronous NLP analysis** with Redis queue and Python worker  
- **Result tracking** in MySQL database, accessible through RESTful APIs  
- **One-click deployment** using Docker Compose  

---

## Architecture Overview

<pre>
                                  +--------------------+
                                  |   Frontend (e.g.,  |
                                  |     Postman / UI)  |
                                  +---------+----------+
                                            |
                                            v
                            +-------------------------------+
                            |      Java Spring Boot         |
                            |   - /api/search               |
                            |   - /api/result/{taskId}      |
        [MySQL DB]<-------- +-----+-------------------------+
Polling and save results          ^     ^
                                  |     | Redis Queue (tasks)
                                  |     v
                                  |   [Redis] <---------+ worker take work
Asynchronous submission of tasks  |                     | update task status
                                  |                     v
                                  |             Python NLP Worker
                                  |                     
                                  v
                              Python Crawler
</pre>

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/AGoodName244/News-and-Opinion-Analysis.git
cd news-nlp-system
```

### 2. Launch All Services

```bash
docker compose up --build
```

This will build and start:
- `nlp-task-dispatcher` (Java backend on port 8080)
- `python-crawler` (crawler service on port 8002)
- `python-nlp` (NLP worker on port 8001)
- Redis (port 6379)
- MySQL (port 3306)

---

### 3. Usage

#### Submit a Search Task

**Endpoint**: `POST /api/search`  
**Content-Type**: `application/json`

Example `curl` command:

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "tiktok", "depth": "shallow"}'
```

Example JSON request body:

```json
{
  "keyword": "tiktok",
  "depth": "shallow"
}
```

**Example Response**:

```json
{
  "taskId": "a1b2c3d4-5678-90ef-...",
  "keyword": "tiktok",
  "depth": "shallow",
  "status": "processing",
  "timestamp": "2025-05-04T13:30:00Z"
}
```

---

#### Query Task Results

**Endpoint**: `GET /api/result/{taskId}`

```bash
curl http://localhost:8080/api/result/a1b2c3d4-5678-90ef
```

If the task is still processing, the API returns an empty array. Once processing is complete, it returns a list of article results including:

- `title`
- `url`
- `summary`
- `sentiment`
- `extracted keywords`

---

### 4. Project Structure

```
news-nlp-system/
├── nlp-task-dispatcher/    # Java: task manager, API, DB, async controller
├── python-crawler/         # Python: fast crawler service
├── python-nlp/             # Python: NLP analysis (keywords, sentiment, summary)
├── shared/                 # Common schemas / test input / docs
├── docker-compose.yml      # Service orchestration
└── README.md
```

---

### 5. Technologies

- **Backend**: Java 17, Spring Boot  
- **Crawling**: Python, newspaper3k  
- **NLP**: Python, Hugging Face Transformers, NLTK / TextBlob  
- **Message Queue**: Redis  
- **Database**: MySQL 8  
- **Deployment**: Docker + Docker Compose  

---

### 6. Notes

- The Java backend handles task submission and polling  
- Tasks are distributed to the Python NLP service via Redis queue  
- NLP results are stored in MySQL only after full task completion  
- Task statuses are tracked in Redis as `processing`, `done`, etc.