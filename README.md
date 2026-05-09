# QA Automation Framework

[![CI](https://github.com/itsDeyvixd/qa-automation-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/itsDeyvixd/qa-automation-framework/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0a9edc?logo=pytest)](https://pytest.org)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen)](reports/coverage/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A professional **API test automation framework** built with Python, Pytest, and GitHub Actions CI/CD. Designed to demonstrate QA engineering best practices including schema validation, data-driven testing, and automated reporting.

---

## Features

- **REST API testing** against [ReqRes.in](https://reqres.in) — a public mock API with users, auth, and resources
- **JSON Schema validation** on every response contract
- **Faker-powered test data** — no hardcoded strings, no false positives
- **Custom assertion helpers** with descriptive failure messages
- **Response time assertions** — performance SLAs enforced in CI
- **Smoke / Regression / Negative** test markers for flexible execution
- **GitHub Actions pipeline** — smoke tests gate the full regression suite
- **Allure + HTML reports** with screenshots and test history
- **Docker support** for reproducible local and CI environments

---

## Project structure

```
qa-automation-framework/
├── .github/workflows/ci.yml   # CI pipeline (smoke → regression → lint)
├── src/
│   ├── api_client.py          # Base HTTP client with logging
│   ├── schemas/api_schemas.py # JSON Schema contracts
│   └── utils/
│       ├── assertions.py      # Custom assertion helpers
│       └── data_factory.py    # Faker-based test data generators
├── tests/
│   ├── conftest.py            # Shared fixtures (client, auth token)
│   └── api/
│       ├── test_users.py      # 20+ CRUD test cases
│       ├── test_auth.py       # 14+ login / register test cases
│       └── test_resources.py  # 10+ resource endpoint test cases
├── pytest.ini                 # Test discovery, markers, coverage config
├── requirements.txt
└── Dockerfile
```

---

## Quick start

### Prerequisites
- Python 3.11+
- pip

### Install and run

```bash
# 1. Clone the repository
git clone https://github.com/itsDeyvixd/qa-automation-framework.git
cd qa-automation-framework

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env

# 5. Run the full suite
pytest
```

### Run specific test subsets

```bash
# Smoke tests only (fast, runs in ~10s)
pytest -m smoke

# Auth tests only
pytest -m auth

# Negative/edge cases only
pytest -m negative

# Exclude performance tests
pytest -m "not performance"

# With verbose output
pytest -v --tb=long
```

### Run with Docker

```bash
docker build -t qa-framework .
docker run qa-framework

# Or run a specific marker
docker run qa-framework pytest -m smoke
```

---

## Test coverage

| Endpoint | Test cases | Coverage |
|---|---|---|
| `GET /users` | 7 | Status, schema, pagination, performance |
| `GET /users/{id}` | 7 | Status, schema, 404, data integrity |
| `POST /users` | 7 | 201, schema, uniqueness, timestamps |
| `PUT/PATCH /users/{id}` | 6 | 200, schema, partial update |
| `DELETE /users/{id}` | 2 | 204, empty body |
| `POST /login` | 10 | Token, schema, missing fields, invalid creds |
| `POST /register` | 7 | 200, schema, error handling |
| `GET /unknown` | 5 | Status, schema, pagination |
| `GET /unknown/{id}` | 7 | Status, schema, data types, 404 |
| **Total** | **56** | |

---

## CI pipeline

Every push triggers this workflow:

```
push / PR
    │
    ▼
 Smoke tests  ──[fail]──▶  ✗ blocked
    │
   [pass]
    │
    ▼
 Regression + Coverage
    │
    ├── Upload test report artifact
    └── Upload coverage to Codecov
    │
    ▼
 Lint (flake8)
```

---

## Key design decisions

**Why an `APIClient` wrapper?**  
Centralises headers, timeouts, and logging. Swapping from staging to production URL is a single environment variable change.

**Why JSON Schema validation?**  
Field-by-field assertions break silently when the API adds new required fields. Schemas catch contract drift and document the expected response shape as code.

**Why Faker for test data?**  
Hardcoded emails like `test@test.com` accumulate state in real APIs. Dynamic data isolates each test run.

---

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Language |
| Pytest | Test runner |
| Requests | HTTP client |
| jsonschema | Response contract validation |
| Pydantic | Data models |
| Faker | Test data generation |
| Allure | Rich test reports |
| GitHub Actions | CI/CD |
| Docker | Reproducible execution |

---

## Author

**Deyvi Ardila** — QA Engineer transitioning into automation and full-stack development.

[![GitHub](https://img.shields.io/badge/github-itsDeyvixd-181717?logo=github)](https://github.com/itsDeyvixd)
