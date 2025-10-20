Purpose
-------
These short instructions help an AI coding agent get productive quickly in this repository ("brief_kg_medaillon"). They focus on the concrete, discoverable shapes and developer workflows I could find by reading the workspace.

Quick summary of repository state
---------------------------------
- Top-level files discovered: `docker-compose.yml`, `readme.txt`, `.gitignore` and a `.git/` folder.
- Both `docker-compose.yml` and `readme.txt` are currently empty in this copy of the repository. There are no source directories or test folders present to inspect.

What an agent should do first (core checklist)
--------------------------------------------
1. Inspect `docker-compose.yml` (open it). If it is empty, look for other branches or the remote repository for a non-empty version.
2. Search for environment files (`.env`, `.env.*`) and CI configuration files (`.github/workflows/**`) — those will reveal runtime services, secrets usage, and build/test commands.
3. If `docker-compose.yml` contains services, extract: service names, images/build contexts, mounted volumes, exposed ports, and environment keys. Use those to infer local run commands.
4. If files are missing (like here), ask the human owner for the intended services and any missing docs before making behavioral changes.

Architecture & intent (how to reason about the repo)
---------------------------------------------------
- Expect a small, service-oriented project anchored around Docker Compose (one or more containers orchestrated locally). The authoritative runtime configuration should be `docker-compose.yml`.
- Look for these typical indicators to map components: service names in the compose file, port mappings (host:container), and mounted volumes (source=local path). Those show boundaries and where code lives.

Developer workflows and useful commands
-------------------------------------
- Common Docker Compose commands to try when the compose file is present:
  - `docker compose up --build` — build and run all services (use this to reproduce local dev environment).
  - `docker compose up -d` and `docker compose logs -f <service>` — run in background and stream logs.
  - `docker compose ps` — list running services and their states.
- If you need to inspect a service container: `docker compose exec <service> /bin/sh` (or `/bin/bash` if available).
- If tests or language-specific tooling are discovered later, follow the commands declared in `README`, `package.json`, `pyproject.toml`, or CI workflow files.

Project-specific conventions and patterns (what I could discover)
----------------------------------------------------------------
- No project-specific patterns were discoverable from the repository contents available here (empty compose/readme). Until more files are present, treat this as a minimal Docker Compose-centered repo.
- When adding code, prefer adding a root README with: how to run (compose), list of services, important env vars, and ports. This accelerates future agents.

Integration points and external dependencies
------------------------------------------
- Look for `image:` fields in `docker-compose.yml` to find external images; `build:` contexts often point to local service code.
- Environment variable keys (for example `DATABASE_URL`, `REDIS_URL`, `AWS_*`) usually indicate external integrations — record them in the README when found.

When to ask the human owner
---------------------------
- The compose file or README is empty (as it is now) — ask which services should run locally, which ports to expose, and whether secrets are stored in an `.env` file or in a secrets manager.
- If you plan to create or modify services, confirm the intended language/runtime (Node, Python, Java, etc.) and the CI/test commands to add.

Examples from this workspace
---------------------------
- Observed files: an empty `docker-compose.yml` at repository root. Because it's empty, the next agent action is to request the missing configuration or check the remote repository/branches.

Notes for merging or updating this file
-------------------------------------
- If a previous `.github/copilot-instructions.md` exists, preserve any explicit step-by-step run commands and only add missing, factual details discovered here.

If anything is unclear or you want the document expanded with run/test examples for a specific language or service, tell me which services (example: PostgreSQL + FastAPI) and I will extend this file with concrete commands and checks.

Optional stack examples (copyable scaffolds)
-------------------------------------------
These tiny examples show how to structure `docker-compose.yml` services and useful local commands. Only add them when the repo intends to use the stack.

- PostgreSQL + FastAPI (recommended layout)
  - service names: `api`, `db`
  - minimal local checks:
    - `docker compose up --build` then `curl http://localhost:8000/health`
    - run DB migrations inside the `api` container: `docker compose exec api alembic upgrade head`
  - typical files to look for: `api/pyproject.toml` or `api/requirements.txt`, `alembic/`, `api/app/main.py`

- Node (Express) + Postgres + Redis
  - service names: `api`, `db`, `redis`
  - minimal local checks:
    - install deps in repo (if node project present): `npm install`
    - start dev server: `npm run dev` (or `node ./bin/www` depending on project)
    - use `docker compose up db redis` to bring dependencies up locally while running node server locally

Checking message & completion limits (notes for agents)
-----------------------------------------------------
- Limits are service/provider-specific (rate limits, per-request message size, and max completion length). This repository contains no settings that enforce chat or model limits.
- If you need precise quotas (messages/minute or max tokens per completion), consult the target LLM/chat provider's documentation or the project's CI/CD/infra configs if they call an API (look for `OPENAI_`, `AZURE_`, `HUGGINGFACE_`, `COHERE_`, etc. env keys).
