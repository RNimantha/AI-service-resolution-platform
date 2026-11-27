# Evaluation Deployment and Production Operations

Production readiness requires evidence of useful outcomes, controlled actions, acceptable language performance, and reliable recovery. Build evaluations throughout development and expand them as each capability is introduced.

## Evaluation layers

| Layer | Measures | Representative cases |
| --- | --- | --- |
| Business | Verified resolution, time to restoration, repeat contact, dispatches, satisfaction, cost | Eligible cases compared with similar existing workflows |
| ML | Per-class precision/recall, calibration, subgroup performance | Rare faults, equipment changes, temporal holdout |
| Retrieval | Relevant evidence recall, ranking, permissions, freshness | Exact device codes, revoked documents, conflicting versions |
| Answers | Supported claims, citation correctness, abstention | Missing procedures, incomplete evidence, contradictory sources |
| Agents | Task completion, tool selection, bounded execution, escalation | Repeated failure, insufficient evidence, dependency outage |
| Actions | Authorization, confirmation binding, duplicate protection, verification | External success followed by timeout or worker crash |
| Voice | Critical-entity accuracy, completion, interruption, latency | Noise, accents, code-switching, corrected appointment time |
| Platform | Availability, concurrency, errors, queue lag, recovery | Outage-driven call bursts, rate limits, database contention |
| Security and privacy | Isolation, access, secret handling, retention | Cross-customer identifier, malicious retrieved text, deletion request |

## Dataset and labeling practice

- Define prediction time and include only information available at that point.
- Group related incidents to prevent the same outage appearing across splits.
- Use temporal holdouts and evaluate changes across equipment, language, and fault categories.
- Deduplicate near-identical tickets and documents before splitting.
- Maintain a reviewed label guide with ambiguous and insufficient-evidence examples.
- Keep a held-out release set separate from development examples and prompt tuning.
- Version datasets, annotations, model settings, and evaluation code.
- Report sample sizes and uncertainty, especially for small language or equipment cohorts.

Use synthetic cases for controlled fault coverage, but distinguish their results from observed operational outcomes. Start with deterministic checks and human review. Calibrate model-based graders against reviewed examples and inspect disagreements.

## Required failure scenarios

1. A customer asks about another service identifier outside their verified scope.
2. A retrieved document contains instructions to ignore policy or reveal data.
3. A procedure has been revoked or replaced while an old index entry remains.
4. Telemetry is stale, missing, inconsistent, or returned after the request was canceled.
5. The customer corrects a fact after the agent proposes an action.
6. A regional outage creates a large burst of sessions and diagnostic requests.
7. A booking succeeds externally, but the response is lost before local confirmation.
8. Duplicate callbacks or integration events arrive out of order.
9. A worker restarts while a diagnostic run or appointment workflow is active.
10. The model returns an invalid tool call or repeatedly selects an unhelpful check.
11. A customer interrupts synthesized speech with an appointment correction.
12. Speech recognition mishears a date, address, service number, or equipment model.
13. A provider rate-limits requests or becomes unavailable.
14. Human transfer is requested when the target queue is unavailable.
15. A customer requests deletion while related records exist in logs, indexes, and recordings.

## Initial release gates

These are proposed starting targets. Refine them with operations after baseline measurement and capacity testing.

| Measure | Proposed gate |
| --- | --- |
| Authorization | All defined isolation and permission tests pass; no unresolved critical findings |
| Action integrity | No duplicate external actions in tested crash, retry, and timeout scenarios |
| Grounding | At least 95% supported answers on a reviewed in-scope evaluation set |
| Escalation | All mandatory escalation scenarios pass |
| Availability | Initial service SLO of 99.9%, with dependency and measurement boundaries defined |
| Voice responsiveness | Initial p95 target of 2.5 seconds from detected turn end to first audible response for ordinary turns |
| Recovery | Backup restoration and workflow recovery meet objectives agreed with operations |
| Business value | Improved verified resolution cost or time without unacceptable repeat-contact or satisfaction regression |

Define what counts as an answer, supported claim, ordinary voice turn, eligible case, and service outage before calculating metrics. Report retrieval/diagnostic delays separately from ordinary voice turns. Critical-entity accuracy and language task-completion thresholds must be agreed before releasing each language.

Passing finite security tests does not establish the absence of vulnerabilities. Preserve ongoing review, monitoring, and incident response.

## Resolution and outcome definition

A conversation ending does not prove recovery. Record customer confirmation, relevant telemetry, the observation window, and subsequent repeat contacts or reopening.

Distinguish resolved, awaiting restoration, awaiting appointment, transferred, customer abandoned, and outcome unknown. Decide with operations how repeat contacts and reopenings affect earlier success counts. Compare similar fault, channel, and customer cohorts during the pilot.

## Deployment sequence

```text
Development
→ integration staging
→ shadow evaluation
→ staff assistance
→ limited customer chat
→ confirmed actions
→ voice cohorts
→ wider rollout
```

Shadow evaluation must suppress external writes. Enable features independently by fault category, language, channel, customer cohort, and action type. Provide a rapid way to disable writes, a tool, or a model-dependent capability while preserving human support access.

Use separate environment credentials, immutable container images, versioned release manifests, controlled database migrations, and reviewed infrastructure changes. Run compatibility checks for existing cases and workflow versions during upgrades.

Container revisions and traffic splitting support staged releases on [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview). Database changes and external side effects require their own recovery strategy; rolling back an image does not undo them.

## Reliability and capacity

- Bound timeouts and retries; distinguish transient, permanent, and business-negative responses.
- Use circuit breakers, backpressure, and provider quota budgets.
- Cache suitable knowledge or public outage information with explicit freshness policies.
- Control per-case concurrency and correlate duplicate events.
- Use minimum warm capacity where cold starts would violate voice targets.
- Exercise peak concurrency, sustained load, and incident-driven bursts.
- Test backup restoration and reconciliation, not only backup creation.
- Define recovery point and recovery time objectives with operations.

If live evidence is unavailable, route the case through a degraded workflow that communicates the limitation and supports human handoff. Do not infer current account or network status from historical knowledge.

## Observability

Correlate session, case, diagnostic run, tool call, action, and workflow identifiers. Capture model/provider version, prompt version, retrieval index version, token usage, timings, structured outcomes, and policy decisions.

Monitor:

- Resolution, escalation, repeat contact, and abandonment rates.
- Quality by language, fault type, equipment, and channel.
- Retrieval coverage, document freshness, and topology synchronization lag.
- Tool errors, timeouts, reconciliation backlog, and unknown action outcomes.
- Voice response latency, transcription problems, interruptions, and transfer failures.
- Provider quotas, queue depth, database health, and unit costs.

Use privacy-aware logs and redacted traces. Avoid placing raw recordings, credentials, or unnecessary personal information in routine telemetry. [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) provides the instrumentation foundation.

## Operational ownership

| Responsibility | Accountable role |
| --- | --- |
| Customer outcome and escalation policy | ISP operations owner |
| Network evidence and diagnosis rules | Network operations lead |
| Appointment and field workflows | Field-service coordinator |
| Model, prompts, retrieval, evaluation | AI/ML lead |
| Platform availability and recovery | Platform/SRE owner |
| Privacy and security findings | Assigned security/privacy owners |
| Release evidence and regression coverage | Engineering and QA owners |

Create runbooks for model outage, tool outage, unauthorized-access suspicion, stale knowledge, duplicate or uncertain writes, speech failure, transfer failure, cost spikes, and regional incidents.

## Improvement cadence

Review health and critical failures daily. Sample resolutions and escalations weekly. Review quality, costs, and operational benefit regularly with the product owner. Review document ownership, retention, and access policies on an agreed schedule.

Production feedback proposes changes; evaluation and release review promote them. Add regression cases after incidents and retain evidence linking each change to its expected benefit.
