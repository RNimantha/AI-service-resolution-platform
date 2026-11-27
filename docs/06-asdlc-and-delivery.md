# ASDLC and Engineering Delivery

Apply governance to both the AI system development lifecycle and AI-assisted software delivery. Product runtime agents and coding assistants have different responsibilities, permissions, and environments.

## AI system lifecycle

```text
Problem definition → data governance → baseline
→ experiment → evaluation → deployment
→ monitoring → reviewed improvement
```

| Step | Required output |
| --- | --- |
| Problem definition | Users, supported faults, operational constraints, success metrics |
| Data governance | Source ownership, access, consent, retention, labeling, lineage |
| Baseline | Existing process and simple technical benchmark |
| Experiment | Reproducible run with defined hypothesis and versioned inputs |
| Evaluation | Quality, subgroup, security, reliability, and cost evidence |
| Deployment | Release manifest, staged rollout, recovery plan, ownership |
| Monitoring | Outcome measures, drift signals, alerts, review cadence |
| Improvement | Reviewed proposal, updated evaluation cases, controlled release |

## AI-assisted software delivery

```text
Requirement → acceptance criteria → design
→ AI-assisted implementation → automated checks
→ human review → staging → release → observation
```

AI can help draft specifications, implement code, investigate failures, and summarize evidence. Engineers remain responsible for accepting the requirement, reviewing changes, judging evaluation results, and owning the service.

Use bounded development tasks with explicit completion criteria. Give coding tools the repository instructions, relevant interfaces, representative fixtures, and commands needed to verify the task. Apply normal secret handling and environment access controls.

## Change evidence

Every production change should include:

- The concrete problem and expected resulting behavior.
- Acceptance criteria and affected users or workflows.
- Relevant code, data, model, prompt, tool, and policy changes.
- Evaluation and test evidence appropriate to the change.
- Compatibility considerations for ongoing cases and workflows.
- Deployment, monitoring, and rollback or recovery instructions.
- Known limitations that materially affect release decisions.

Keep architecture decisions in short records explaining context, decision, alternatives, tradeoffs, and revisit conditions. Describe the final design rather than the history of drafts.

## Release manifest

Link these artifacts for every production release:

```text
Code commit and container digest
Database schema version
Model identifiers and inference settings
Prompt versions
Tool schemas and executor version
Workflow versions and runtime policies
Embedding model and retrieval index version
Source document and dataset snapshots
Evaluation dataset, code, and results
Deployment configuration and feature flags
```

Store configuration and artifact references so that production behavior can be investigated later. Restrict access to sensitive inputs; reproducibility does not require copying customer data into unrestricted logs.

## CI and release pipeline

```text
Change proposed
→ lint, typing, unit and contract checks
→ relevant model, retrieval, agent, and security evaluations
→ build and scan immutable images
→ deploy staging and run integration checks
→ review release evidence
→ enable controlled production cohort
→ observe metrics and expand or recover
```

Choose checks by the affected capability. A prompt change may require answer and agent regressions; a tool change requires contract, authorization, and side-effect checks; a migration requires compatibility and recovery validation.

Human confirmation within the product is an operational policy for customer actions. It is distinct from engineering review of a production software release.

## Application structure

One application owns its dependencies through the root pyproject.toml and uv.lock. Its execution entry point is src/main/app/main.py.

```text
src/main/app/
├── main.py
├── controller/
│   ├── app_factory.py
│   ├── router.py
│   ├── health_controller.py
│   ├── schemas/
│   ├── dependencies/
│   └── middleware/
├── core/
│   └── composition.py
├── shared/
│   └── contracts/
└── services/
    ├── rag_service/
    ├── agent_service/
    ├── context_service/
    ├── tool_service/
    ├── case_service/
    ├── workflow_service/
    ├── speech_service/
    ├── ml_service/
    └── topology_service/
```

All HTTP framework code belongs to controller. Business services and shared contracts remain framework-independent. Public imports use paths such as from src.main.app.services.rag_service import RagService. Each Python file defines at most one class and contains no more than 749 physical lines.

The scaffold provides process liveness and preserves the injectable RAG components. Operational providers, authenticated business endpoints, and deployment remain implementation work. See [the structure guide](08-project-structure.md) for ownership, imports, and execution commands.

Keep production customer data, recordings, secrets, and model weights out of source control. Version dataset manifests and artifact references instead.

## Decisions to resolve during inception

| Decision | Required evidence | Owner |
| --- | --- | --- |
| Supported customer and service scope | Operational workflow and access model | Product and operations |
| Approved vendor processing and region | Data classification and service capability checks | Security/privacy and platform |
| Identity and verification integration | Existing ISP identity flows and sandbox validation | Backend and identity owner |
| Selected model identifiers | Project benchmark and provider terms | AI/ML lead |
| Speech languages and telephony path | Representative audio and carrier feasibility | Voice and operations owners |
| Metric thresholds and observation windows | Baseline data and risk tolerance | Product, operations, and QA |
| Recovery objectives | Business impact and restoration experiments | Operations and platform |
| Graph infrastructure expansion | Query complexity, load, and maintenance evidence | Architecture owner |

Record decisions as they are made, and update affected documentation and release criteria together.
