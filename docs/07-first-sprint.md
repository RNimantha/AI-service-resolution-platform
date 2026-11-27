# First Two Week Sprint

The first sprint establishes an agreed product scope, a route to real integrations, baseline evidence, and a small engineering foundation. It does not require building an autonomous agent.

## Sprint outcome

By the end of the sprint, the team should be able to explain the customer journey, demonstrate a minimal staging service, identify integration owners, and use reviewed scenarios to judge future behavior.

## Backlog

| Item | Work | Deliverable | Acceptance criteria |
| --- | --- | --- | --- |
| Product scope | Review the three initial fault categories and current support process | Scope and workflow map | Operations accepts supported issues, exclusions, handoff, and resolution definition |
| Integration inventory | Identify CRM, telemetry, incidents, diagnostics, appointments, and identity systems | Integration register | Each system has an owner, access status, interface description, and next step |
| Sample data | Obtain approved de-identified examples or create clearly marked synthetic fixtures | Sample dataset and source manifest | Fields, provenance, access, and permitted use are documented |
| Labeling guide | Define issue labels, outcomes, ambiguity, and insufficient evidence | Initial label guide | Domain reviewers resolve representative disagreements |
| Evaluation scenarios | Collect success, escalation, correction, and failure cases | Reviewed scenario set | Expected behavior and prohibited actions are explicit |
| Engineering scaffold | Establish API skeleton, dependencies, container, CI, and basic health check | Repository foundation | A clean checkout can build, check, and run the service |
| Staging path | Provision the smallest approved staging deployment | Staging service | Deployment is repeatable and environment credentials are separated |
| Baseline metrics | Define metrics and identify available historical measurements | Baseline measurement plan | Denominators, windows, and data owners are recorded |
| Voice feasibility | Validate sample audio, streaming access, and contact-center path | Feasibility notes | Language and carrier blockers have an owner and follow-up plan |
| Architecture decisions | Record initial component boundaries and unresolved choices | Decision records | Each open dependency has an owner and decision date |

## Suggested sequence

| Days | Focus |
| --- | --- |
| 1–2 | Stakeholder interviews, workflow review, scope, integration ownership |
| 3–4 | Sample data access, labeling guide, customer verification, privacy constraints |
| 5 | Initial scenario review and architecture decisions |
| 6–7 | API scaffold, CI, container, local setup |
| 8 | Minimal staging deployment and repeatability check |
| 9 | Speech and integration feasibility review; resolve or assign dependencies |
| 10 | Demonstration, artifact review, acceptance, and next-sprint planning |

These are working-day allocations. Run access requests in parallel with documentation and scaffolding work so that external approvals do not consume the whole sprint.

## Initial scenario set

Include at least these categories, with domain-reviewed expected behavior:

1. Known outage affecting the verified service.
2. Intermittent connection with earlier restarts already recorded.
3. Slow connection with incomplete telemetry.
4. Wrong customer or service identifier.
5. Conflicting troubleshooting documents.
6. Customer correction during the conversation.
7. Diagnostic API timeout.
8. Appointment availability changing before confirmation.
9. External booking success followed by a lost response.
10. Mandatory human escalation or customer request for a human.
11. Noisy speech with an uncertain appointment date.
12. Regional incident with many simultaneous contacts.

## Definition of done

- Operations accepts the first-release scope and escalation ownership.
- Integration access has a recorded status, owner, and next action.
- Sample data has a permitted use and is labeled as real de-identified or synthetic.
- The labeling guide and representative scenarios have been reviewed.
- The staging service can be reproduced from source and documented configuration.
- No production customer credentials or recordings are committed to the repository.
- Next-sprint work has explicit acceptance criteria and known dependencies.

## Next sprint

Begin the foundational learning and baseline work in [Phase 1 of the implementation roadmap](04-implementation-roadmap.md#phase-1-software-and-ml-foundations). Engineers who already have these skills can progress data access and the application foundation while documenting the same baseline evidence.
