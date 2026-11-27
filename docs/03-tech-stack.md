# Technology Stack and Resource Plan

Use Azure for the primary infrastructure and keep business logic behind portable Python interfaces. Introduce specialized infrastructure when a measured requirement justifies it.

## Application and AI stack

| Area | Default choice | Purpose and adoption |
| --- | --- | --- |
| Backend | Python, uv, FastAPI, Pydantic | Typed APIs, streaming, orchestration, and ML |
| Frontend | Next.js, React, TypeScript | Customer chat and support console |
| Persistence | SQLAlchemy, Alembic | Database access and migrations |
| Operational database | Azure Database for PostgreSQL | Cases, actions, conversations, permissions, outcomes |
| Retrieval | PostgreSQL full-text search and pgvector | Hybrid search without a separate initial search service |
| Files and datasets | Azure Blob Storage and Parquet | Source documents, recordings where permitted, snapshots, artifacts |
| Traditional ML | scikit-learn and XGBoost | Classifiers and fault prediction |
| Deep learning | PyTorch and Transformers | Learning exercises and benchmark-driven adaptation |
| Embeddings | Sentence Transformers with BGE-M3 as a baseline | Multilingual retrieval candidate |
| Generation | Claude API behind an application adapter | Structured extraction, diagnosis, explanation |
| Diagnostic graph | LangGraph with PostgreSQL checkpoints | Diagnostic flow and conversation continuity |
| Durable workflows | Temporal Cloud | Add for appointments and restoration follow-up |
| Network graph | PostgreSQL edge tables | Begin here; introduce Neo4j for demonstrated traversal needs |
| Speech | Azure Speech STT and TTS | Language-gated streaming speech |
| Telephony | Existing ISP integration; Twilio Media Streams reference adapter | Validate carrier connectivity before production selection |
| Messaging | Azure Service Bus | Ingestion and integration events |
| Experiment tracking | MLflow | ML runs, model versions, evaluation artifacts |

## Platform and delivery stack

| Area | Default choice | Purpose |
| --- | --- | --- |
| Containers | Docker and Azure Container Registry | Reproducible images and image distribution |
| Hosting | Azure Container Apps | API, web, ingestion, and workflow worker deployment |
| Infrastructure | Terraform | Repeatable environments and controlled changes |
| CI/CD | GitHub Actions | Checks, artifacts, staging, and deployment |
| Staff identity | OIDC with the ISP identity provider | Staff roles and session security |
| Customer identity | Existing ISP verification or portal identity | Bind service access to verified customers |
| Secrets | Azure Key Vault and managed identities where available | Credential storage and service access |
| Observability | OpenTelemetry and Azure Monitor | Traces, metrics, logs, alerts |
| Tests | pytest, Playwright, Locust | Unit, integration, browser, concurrency, and load checks |

Use a modular backend and a small set of workers initially. Kubernetes, Kafka, a separate vector database, and a dedicated feature store are later architecture decisions if capacity or operational requirements demand them.

## Model selection

Benchmark candidate models using the project's reviewed support cases. Evaluate structured-output correctness, tool selection, grounding, local-language quality, latency, cost, and behavior under missing evidence.

Pin the selected model identifier, inference settings, prompt version, embedding model, and library versions. Assess data processing terms, retention, licensing, and approved regions before sending customer information to a vendor.

BGE-M3 is a multilingual retrieval candidate, not a guarantee of adequate Sinhala or Tamil retrieval. Test local-language queries, equipment codes, and code-switching. [Model card](https://huggingface.co/BAAI/bge-m3)

Fine-tune only when an evaluated error pattern, suitable labeled data, and a measurable benefit justify it. Small neural-network learning exercises do not need to become production services.

## Staged adoption

| Stage | Introduce |
| --- | --- |
| Foundation | Python, API, PostgreSQL, Blob Storage, CI, identity, initial staging |
| ML | scikit-learn, XGBoost, MLflow, reproducible datasets |
| RAG | Document ingestion, embeddings, full-text and vector retrieval |
| Conversation and diagnosis | LangGraph, context assembly, tool executor, runtime budgets |
| Controlled actions | Action ledger, outbox, reconciliation, Temporal |
| Voice | Speech, audio gateway, contact-center adapter |
| Scale when justified | Neo4j, dedicated inference capacity, additional independently scaled services |

## Team coverage

| Responsibility | Suggested coverage |
| --- | --- |
| Architecture, ML, RAG, agents | AI/ML lead and applied AI engineer |
| APIs, integrations, durable actions | Backend/integration engineer |
| Customer and staff experiences | Frontend engineer |
| Infrastructure, reliability, delivery | Platform/SRE engineer |
| Labels, workflow acceptance, operational decisions | ISP operations owner and domain reviewers |
| Release qualification | QA support and security review at relevant gates |

People may cover multiple roles. Access to domain experts and integration owners is necessary regardless of engineering team size.

## Cost and capacity planning

Estimate monthly operating cost from measured workload:

```text
LLM input and output usage
+ embedding and reranking inference
+ STT audio duration
+ TTS generation
+ telephone minutes
+ application and worker compute
+ databases, storage, networking, and observability
+ operational support
```

Track both cost per eligible case and cost per verified resolution. Model retries, long calls, failed cases, recordings, and traces all consume resources.

Create a capacity model covering concurrent sessions, call duration, turns per case, tool calls, provider quotas, ingestion volume, and incident-driven bursts. Validate cold-start and scaling behavior before choosing minimum warm capacity for voice. Check current vendor prices and account quotas when budgeting rather than treating this plan as a pricing estimate.

## Technology references

- [pgvector hybrid search](https://github.com/pgvector/pgvector) describes combining vectors with PostgreSQL full-text search and rank fusion or reranking.
- [Azure PostgreSQL extensions](https://learn.microsoft.com/en-us/azure/postgresql/extensions/concepts-extensions-versions) lists available extensions and versions; verify the selected server configuration.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) distinguishes graph checkpoints from longer-term stores.
- [Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) describes model tool interactions; the application still enforces authority.
- [Temporal Activities](https://docs.temporal.io/activities) explains idempotency expectations around retries.
- [Azure Speech language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) distinguishes language coverage by feature and locale.
- [Twilio Media Streams](https://www.twilio.com/docs/voice/media-streams) describes real-time audio streaming integration.
- [MLflow tracking](https://mlflow.org/docs/latest/tracking/) and [model registry](https://www.mlflow.org/docs/latest/registry/) cover experiment and model lifecycle records.
- [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) provides telemetry concepts and instrumentation guidance.
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview) documents container hosting, scaling, revisions, and traffic splitting.
