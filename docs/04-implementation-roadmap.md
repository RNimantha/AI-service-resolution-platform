# Implementation Roadmap from ML Basics to Production

Follow the phases in dependency order and use each exit gate to decide whether to proceed. Evaluation, access control, CI, and observability begin early and expand with the product.

## Reference schedule

| Phase | Weeks | Main result |
| --- | --- | --- |
| 0 Product definition and access | 1–2 | Agreed scope and integration plan |
| 1 Software and ML foundations | 3–6 | Reproducible baseline classifier |
| 2 Data and application foundation | 7–9 | Ingestion, identity, schema, staging |
| 3 Traditional ML | 10–12 | Evaluated classification and fault models |
| 4 Deep learning and model selection | 13–14 | Benchmarked language and embedding models |
| 5 Prompt engineering and RAG | 15–18 | Staff knowledge assistant |
| 6 Context and conversation | 19–21 | Resumable evidence-aware conversations |
| 7 Graph engineering | 22–24 | Diagnostic and topology graphs |
| 8 Tools, agents, loops, and harness | 25–28 | Read-only diagnostic agent |
| 9 Controlled actions and durability | 29–31 | Recoverable tickets and appointments |
| 10 Speech and telephony | 32–35 | Evaluated voice capability |
| 11 System qualification | 36–38 | Release evidence and recovery tests |
| 12 Production pilot | 39–42 | Controlled deployment and business results |
| 13 Operations and improvement | Ongoing | Monitored, governed improvement |

These 42 sequential weeks include foundational learning and are an illustrative planning reference. Run access procurement and feasibility work early. An experienced team may overlap frontend, integration, data, and platform work; beginners should allow additional learning time.

## Phase 0 Product definition and access

**Weeks 1–2.** Establish the operational problem, authority boundaries, and evidence needed to judge success.

Work:

- Interview support, network, and field-service teams.
- Map current workflows for no connection, intermittent connection, and slow connection.
- Identify API owners, sandboxes, quotas, connectivity, and production access requirements.
- Define verification, staff roles, permitted actions, confirmation, and escalation ownership.
- Agree on data retention, recording consent, and vendor processing requirements.
- Run feasibility checks for speech, telephony, and network access.
- Record current resolution time, repeat contacts, dispatches, and handling costs.

Deliverables: product requirements, acceptance criteria, workflow maps, integration inventory, data classification matrix, architecture decisions, and business baseline.

Exit gate: an operations owner accepts scope, and real data and integration access have a credible path with named owners. Use simulators while access is pending.

## Phase 1 Software and ML foundations

**Weeks 3–6.** Apply foundational concepts to support cases.

Learn Python, SQL, Git, HTTP, asynchronous programming, automated testing, NumPy, and pandas. Study vectors, similarity, probability, statistics, optimization, classification, regression, regularization, overfitting, and data leakage. Understand precision, recall, F1, calibration, and uncertainty.

Build an exploratory analysis of de-identified or synthetic tickets, a rule-based classifier, a TF-IDF plus logistic regression classifier, and a small prediction API.

Deliverables: dataset description, exploratory analysis, reproducible training script, confusion matrix, baseline report, and tested prediction endpoint.

Exit gate: another engineer can reproduce the experiment, and its errors and operational limitations are explained.

## Phase 2 Data and application foundation

**Weeks 7–9.** Establish the engineering foundation before introducing agents.

Work:

- Create repository structure, dependency locks, CI, linting, typing, and meaningful tests.
- Containerize development and deploy an initial staging service.
- Integrate customer and staff identity.
- Implement core schema, migrations, audit events, and customer isolation.
- Ingest tickets, approved manuals, inventory, and telemetry.
- Validate, deduplicate, redact, and track data lineage.
- Version dataset snapshots and establish a labeling workflow.
- Build integration simulators with realistic errors and timeouts.

Deliverables: data dictionary, entity model, ingestion jobs, labeling guide, reviewed seed dataset, integration simulators, and authenticated staging application.

Exit gate: ingestion failures are visible, records have provenance, and customer isolation is tested.

## Phase 3 Traditional ML models

**Weeks 10–12.** Use ML where it improves an operational decision.

| Task | Baseline and candidate | Intended use |
| --- | --- | --- |
| Issue classification | Rules, TF-IDF/logistic regression, embedding classifier | Route a case |
| Likely fault category | Rules, then XGBoost using available telemetry | Prioritize checks |

Define prediction time and feature availability. Group related incidents and evaluate on temporal holdouts. Exclude facts available only after resolution. Address imbalance, evaluate subgroups, and calibrate predictions. Include an insufficient-evidence outcome.

Deliverables: feature definitions, feature pipeline, training/evaluation jobs in MLflow, model cards, calibration results, thresholds, and versioned inference endpoint.

Exit gate: the selected model improves the agreed decision metric without unacceptable subgroup regressions. Retain the baseline when a more complex model does not help.

## Phase 4 Deep learning and language model selection

**Weeks 13–14.** Connect neural-network concepts to model selection.

Learn tensors, gradients, loss, backpropagation, tokenization, embeddings, attention, transformer architecture, context limits, sampling, structured output, and inference cost. Distinguish pretraining, fine-tuning, and retrieval augmentation.

Build a small neural classifier as a learning exercise, compare a pretrained transformer classifier, benchmark embedding retrieval, and evaluate candidate generative models on reviewed support cases.

Deliverables: quality/latency/resource/cost comparison, model-selection decision, provider adapter with normalized errors and timeouts, and model licensing review.

Exit gate: choices follow measured requirements. Fine-tuning is a separate experiment when a failure pattern and suitable data justify it.

## Phase 5 Prompt engineering and RAG

**Weeks 15–18.** Release a useful knowledge assistant to support staff.

Work:

- Extract or OCR approved documents and preserve meaningful structure.
- Chunk with equipment, language, owner, version, effective-date, and permission metadata.
- Build embeddings, keyword search, rank fusion, and optional reranking.
- Enforce access during retrieval and test revocation and deletion propagation.
- Version prompts for extraction, clarification, grounded answers, and abstention.
- Validate structured model output in application code.
- Compare keyword-only, vector-only, and hybrid retrieval.
- Add a staff console showing source references and supporting passages.

Deliverables: ingestion service, retrieval API, source viewer, prompt library, reviewed question set, evaluation report, and staff console.

Exit gate: reviewers accept performance on supported questions, missing evidence, conflicting guidance, and outdated documents.

## Phase 6 Context engineering and conversation

**Weeks 19–21.** Make conversations dependable across turns and sessions.

Build a context assembler for verified scope, symptoms, facts with provenance, completed actions, unresolved questions, relevant procedures, permitted tools, and remaining budget. Implement token budgets, summaries, freshness rules, correction handling, conversation resumption, and channel switching.

Preserve important details such as previous router restarts. Distinguish customer reports from live observations. Build human handoffs containing evidence, completed work, outstanding questions, and next steps.

Deliverables: context schema and assembler, memory retention/deletion rules, conversation simulator, handoff format, and regression cases for long histories and corrections.

Exit gate: relevant facts survive summarization, stale data is refreshed, and completed troubleshooting is not repeated without a reason.

## Phase 7 Graph engineering

**Weeks 22–24.** Implement diagnostic control flow and network relationships as separate models.

Build the diagnostic graph with verification, classification, outage checks, evidence collection, retrieval, next-step selection, questions, permitted diagnostics, outcome checks, and escalation.

Model service-to-device-to-network relationships with provenance and validity periods. Query shared assets, affected services, relevant incidents, and correlated complaints. Start with bounded PostgreSQL queries; benchmark Neo4j when needed. Measure graph-assisted retrieval before broad GraphRAG adoption.

Deliverables: executable diagnostic graph, topology schema, synchronization process, tested relationship queries, freshness rules, and retrieval comparison.

Exit gate: graph results improve defined diagnostic tasks and inferred hypotheses remain distinct from observed relationships.

## Phase 8 Tools agents loops and harness

**Weeks 25–28.** Implement one diagnostic agent within the deterministic workflow, beginning with read-only access.

Work:

- Implement service status, outages, telemetry, device, existing-case, and approved line-test tools.
- Define typed contracts, permissions, timeouts, error types, sensitivity, and retry behavior.
- Derive customer scope from the authenticated session.
- Implement the observe/select/execute/validate/update loop.
- Bound steps, elapsed time, tokens, cost, repeated actions, and output repair.
- Detect stalled progress and provide cancellation and per-case concurrency control.
- Trace tool results, model usage, evidence updates, and termination reasons.
- Evaluate success, missing evidence, injection attempts, and dependency failures.

Deliverables: tool registry, executor, diagnostic agent, harness configuration, failure simulator, and evaluation report.

Exit gate: supported cases complete within their budgets; failures terminate or escalate predictably; unauthorized access tests pass.

## Phase 9 Controlled actions and durable workflows

**Weeks 29–31.** Add external writes with confirmation and recovery.

Build ticket creation, incident linking, appointment availability, reservation, confirmation, and cancellation. Bind confirmation to the exact action, customer, case, and expiry. Recheck authority and preconditions before execution.

Introduce Temporal for appointments and restoration follow-up. Implement an action ledger, transactional outbox, idempotency keys, external identifiers, reconciliation, and operator recovery. An uncertain result must be reconciled before repeating the write.

Deliverables: confirmed-action API, durable workers, appointment integration, reconciliation jobs, and stalled-case interface.

Exit gate: crash, timeout, retry, and stale-confirmation scenarios recover without duplicate appointments or tickets.

## Phase 10 Speech and telephony

**Weeks 32–35.** Validate browser voice before connecting live customer calls.

Work:

- Implement streaming audio, transcription, turn detection, and speech synthesis.
- Handle interruptions, cancel stale generation, and stop playback.
- Confirm uncertain names, dates, addresses, and appointment details.
- Handle codecs, buffering, backpressure, reconnect, and session expiry.
- Transfer calls to humans with case context.
- Apply recording consent, access, and retention rules.
- Evaluate English, Sinhala, Tamil, accents, noise, and code-switching separately.

Deliverables: browser voice interface, telephone adapter, consented speech corpus, language reports, latency and transfer tests, and fallback procedures.

Exit gate: every released language meets task-completion, critical-entity accuracy, and responsiveness criteria. Feature support alone is insufficient evidence of language quality.

## Phase 11 System evaluation and reliability qualification

**Weeks 36–38.** Consolidate the evaluation suites built in earlier phases.

Test held-out ML quality, retrieval access control, grounded answers, agent termination, authorization, action integrity, voice completion, integration failures, peak load, and recovery. Include regional outage bursts and a worker crash immediately after an external booking succeeds.

Use deterministic assertions, human review, and model-based graders together. Exercise backup restoration and define recovery objectives with operations.

Deliverables: qualification suite, threat model, security findings, load and soak reports, recovery evidence, known limitations, and release decision.

Exit gate: material findings are resolved, and operations accepts the residual limitations and escalation procedures.

## Phase 12 Production deployment and pilot

**Weeks 39–42.** Release by cohort, language, issue category, channel, and action.

Deployment sequence:

```text
Development → integration staging → shadow evaluation
→ staff assistance → limited customer chat
→ confirmed actions → voice cohorts → wider rollout
```

Provision separate environments and credentials with Terraform. Deploy immutable containers, test database migrations, validate private connectivity and provider quotas, configure circuit breakers and warm capacity, and exercise rollback.

Create dashboards, alerts, on-call responsibilities, operational runbooks, and incident ownership. Compare pilot outcomes with the existing workflow using similar cohorts and an agreed evaluation window.

Deliverables: production deployment, pilot report, rollback and recovery evidence, support documentation, and expansion decision.

Exit gate: measured business value accompanies acceptable quality, reliability, privacy, and cost.

## Phase 13 Operations and improvement

**Ongoing.** Review service health and failure patterns daily; sample resolutions and escalations regularly. Track language, device, fault, and channel performance, document freshness, topology lag, provider changes, and unit costs.

Expand reviewed labels and evaluation sets. Use champion/challenger experiments for models, prompts, and retrieval changes. Route all production updates through evaluation and release gates. Add regression cases after incidents.

Deliverables: recurring quality/cost reports, incident reviews, updated datasets, evaluated release candidates, and a prioritized improvement backlog.

Exit criteria apply to individual releases. Operating a production service remains an ongoing responsibility.
