# AI Service Resolution Platform

A production implementation plan for a multilingual broadband support platform that takes a customer from an initial call or chat through diagnosis, authorized action, human escalation, and verified service recovery.

Created: 22 November 2026  
Status: Modular application scaffold and implementation documentation  
Primary infrastructure: Azure  
Reference schedule: 42 sequential weeks, followed by ongoing operations

## Project outcome

Reduce the cost and time required to restore broadband service while maintaining customer satisfaction, privacy, and operational safety. Measure verified resolutions and repeat contacts rather than treating a conversation ending as a successful resolution.

The initial release supports no connection, intermittent connection, and slow connection for one ISP and one support team. Release staff assistance first, followed by customer chat, controlled actions, and voice. Evaluate English, Sinhala, and Tamil independently before enabling each language for customers.

## Documentation

| Document | Purpose |
| --- | --- |
| [Use case and scope](docs/01-use-case.md) | Business problem, customer journey, capability coverage, and production boundaries |
| [System architecture](docs/02-architecture.md) | Components, data ownership, graphs, context, tools, and durable actions |
| [Technology stack](docs/03-tech-stack.md) | Default technologies, staged additions, selection criteria, staffing, and cost planning |
| [Implementation roadmap](docs/04-implementation-roadmap.md) | Learning objectives, engineering work, deliverables, and exit gates for every phase |
| [Evaluation and operations](docs/05-evaluation-and-operations.md) | Quality measures, reliability, security, deployment, and production operations |
| [ASDLC and delivery](docs/06-asdlc-and-delivery.md) | AI system lifecycle, AI-assisted software delivery, release evidence, and proposed repository structure |
| [First sprint](docs/07-first-sprint.md) | Actionable two-week starting backlog and acceptance criteria |
| [Project structure](docs/08-project-structure.md) | Service folders, package ownership, import examples, and enforced coding rules |
| [RAG micro tasks](docs/09-rag-microtasks.md) | One runnable RAG task at a time, with a user checkpoint before continuing |

## Development setup

The application lives under src/main/app. Business services belong in src/main/app/services; all FastAPI routes, HTTP schemas, dependencies, middleware, and app construction belong in src/main/app/controller. One root pyproject.toml manages dependencies.

```sh
make setup
make check
make run
```

The sole application entry point is [src/main/app/main.py](src/main/app/main.py). The direct module command is `uv run --locked python -m src.main.app.main`. It starts a local API with liveness at /health/live and development documentation at /docs. The first RAG task adds POST /rag/documents/preview for submitted text; production storage, retrieval, and generation remain later work.

Start the guided RAG implementation with [Task 1 text document preview](docs/rag/task-01-text-document-preview.md). Each subsequent task waits for your run and review.

Public imports use the requested namespace:

```python
from src.main.app.services.rag_service import RagService
```

Every Python file defines at most one class and remains below 750 physical lines. See [the structure guide](docs/08-project-structure.md) and [engineering rules](AGENTS.md) for ownership, imports, and checks.

## Delivery milestones

| Milestone | Reference completion | Result |
| --- | --- | --- |
| Product and access established | Week 2 | Agreed scope, integration owners, baseline metrics |
| Reproducible ML baseline | Week 12 | Evaluated classifier and fault prediction experiments |
| Staff knowledge assistant | Week 18 | Permission-filtered RAG with evidence and citations |
| Read-only diagnostic agent | Week 28 | Bounded tool use with traceable evidence and escalation |
| Controlled case actions | Week 31 | Confirmed ticket and appointment actions with recovery |
| Voice capability | Week 35 | Evaluated speech and telephony integration |
| Production pilot review | Week 42 | Measured business, quality, reliability, and cost results |

The schedule includes foundational learning. It is a planning reference rather than a delivery commitment. Experienced teams can overlap workstreams; beginners may require additional learning time. Data access, integration procurement, and operational review can affect the critical path.

## Operating assumptions

- An ISP operations owner and domain reviewers participate throughout implementation.
- Production access follows the ISP's identity, privacy, security, and change-management requirements.
- Synthetic datasets and simulators support development; real operational data and a controlled pilot establish production readiness.
- Model and service selections are candidates until benchmarked and checked against region, language, licensing, and data-processing requirements.
- The modular scaffold includes a FastAPI liveness endpoint, injectable RAG interface, shared request context, checks, and CI. Production providers, business endpoints, frontend, and infrastructure remain implementation work.

Start with [the first sprint](docs/07-first-sprint.md) and use [the roadmap](docs/04-implementation-roadmap.md) to track subsequent phases.
