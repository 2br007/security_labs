# FastAPI Security Laboratory

A hands-on **application security training environment** built with FastAPI, Postgres, and Docker.

This project demonstrates common real-world web vulnerabilities, their exploitation, and secure implementations following OWASP Top 10 practices.

---

## Purpose

This repository is designed to:

- Practice real-world web application vulnerabilities
- Demonstrate exploitation techniques in a controlled environment
- Show secure coding fixes side-by-side
- Simulate an AppSec / Bug Bounty workflow
- Serve as a portfolio project for security engineering roles

---

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker / Docker Compose
- Pytest
- Ruff (linting)
- Bandit (security scanning)
- Semgrep (security scanning)
- Pre-commit hooks
- GitHub Actions CI

---

## Architecture

```
FastAPI App
│
├── vulnerable/ → intentionally insecure endpoints
├── secure/ → fixed implementations
├── db/ → Postgres + SQLAlchemy models
├── core/ → security utilities (auth, rate limiting)
└── tests/ → unit + security tests
```

---

## Implemented Vulnerabilities

Each vulnerability includes:
- vulnerable implementation
- exploit example
- secure fix
- automated tests

### 1. Broken Object Level Authorization (BOLA / IDOR)
- Access other users' data by modifying IDs

```bash
curl -H "X-User-ID: 1" \
http://localhost:8000/vulnerable/users/2
```

Expected result (vulnerable behavior)

```json
{
  "id": 2,
  "username": "bob",
  "email": "bob@test.com"
}
```

- Fix: ownership validation


```bash
curl -H "X-User-ID: 1" \
http://localhost:8000/secure/users/2
{"detail":"Not authorized to access this resource"}
```

### 2. SQL Injection
- Raw SQL string concatenation (Extract all users via injection)

```bash
curl "http://localhost:8000/vulnerable/sqli/search?username=' OR 1=1--"
```

Expected result: Returns all users in database.

Normal request

```bash
curl "http://localhost:8000/vulnerable/sqli/search?username=alice"
```

- Fix: parameterized queries (SQLAlchemy text binding)


```bash
curl "http://localhost:8000/secure/sqli/search?username=' OR 1=1--"

[]
```

### 3. Server-Side Request Forgery (SSRF)
- Fetch internal services via URL parameter


Access external site

```bash
curl "http://localhost:8000/vulnerable/ssrf/fetch?url=https://example.com"
```

Access internal service (attack)

```bash
curl "http://localhost:8000/vulnerable/ssrf/fetch?url=http://localhost:8000/internal/metadata"
```

Result:

Leaks internal secrets:

```json
{
  "service": "internal-metadata",
  "secret_key": "SUPER_SECRET_KEY",
  "db_password": "postgres123"
}
```

- Fix: allowlist + hostname validation

```bash
curl "http://localhost:8000/secure/ssrf/fetch?url=http://localhost:8000/internal/metadata"
{"detail":"URL not allowed"}
```

### 4. Path Traversal
- Read arbitrary filesystem files

Read safe file

```bash
curl "http://localhost:8000/vulnerable/path/read?filename=hello.txt"
```

Access system file (attack)

```bash
curl "http://localhost:8000/vulnerable/path/read?filename=../../../../etc/passwd"
```

Expected result
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
```

- Fix: path resolution + directory confinement


```bash
curl "http://localhost:8000/secure/path/read?filename=../../../../etc/passwd"
```

```json
{"detail":"Access denied"}
```

### 5. Missing Rate Limiting
- Brute-force login attacks

Bruteforce login endpoint

```bash
for i in {1..10}; do
  curl -X POST "http://localhost:8000/vulnerable/auth/login?username=alice"
done
```

Result:
All requests succeed
No blocking
No delay
No throttling

- Fix: in-memory rate limiter (IP-based)


```bash
curl -X POST "http://localhost:8000/secure/auth/login?username=alice"
```

After 3 requests:

```json
{"detail":"Too many requests"}
```

---

## Usage

Start security lab container:
```bash
make lab
```

Stop security lab container:
```bash
make down
```

Run unittests over container:
```bash
make test
```

---

## Other info

### API available at

```
http://localhost:8000
```

### Swagger docs

```
http://localhost:8000/docs
```
