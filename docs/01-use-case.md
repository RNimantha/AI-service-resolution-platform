# Broadband Service Resolution Use Case

Build a multilingual AI Service Resolution Platform for an internet service provider. The platform should help restore service, arrange the next operational step, or transfer a complete case to a human. The customer operations team owns the product with network operations and field service.

## Business problem

Customers repeat their symptoms across channels, support staff search multiple systems, and troubleshooting can overlook existing outages or earlier actions. Unnecessary appointments and incomplete handoffs increase cost and resolution time.

The platform brings documented procedures and current operational evidence into one controlled workflow. Success is a verified service outcome with an auditable record of what happened.

## Initial production scope

| Dimension | Initial scope |
| --- | --- |
| Organization | One ISP and one support team |
| Problems | No connection, intermittent connection, slow connection |
| Users | Customers, support staff, network operations, field service |
| Channels | Staff console, customer chat, then browser and telephone voice |
| Languages | English first; Sinhala and Tamil after separate evaluations |
| Read access | Account scope, relevant devices, outages, telemetry, case history, approved documents |
| Actions | Approved diagnostics, ticket creation, incident linking, confirmed appointment booking |
| Escalation | Insufficient evidence, exhausted diagnostic budget, customer request, tool failure, or policy requirement |
| Resolution | Telemetry and customer evidence evaluated over an agreed observation window |

Infrastructure configuration changes, unrestricted shell access, arbitrary SQL, autonomous refunds, and fleet-wide network remediation are outside the first release. Expand action scope only through an explicit operational release decision.

## Customer journey

The customer says: “My internet keeps disconnecting every evening. I already restarted the router twice.”

1. Transcribe the request or accept chat text and identify the working language.
2. Verify identity before accessing account information.
3. Record symptoms, affected service, and troubleshooting already completed.
4. Check active incidents, relevant equipment, connection telemetry, and existing cases.
5. Retrieve current troubleshooting instructions for the customer's equipment and service.
6. Investigate whether the evidence points toward Wi-Fi, customer equipment, or the provider's network.
7. Ask for missing information and run permitted diagnostics within a bounded loop.
8. Propose an action and obtain confirmation when required.
9. Execute the action through the authorized executor, or transfer the case to a human.
10. Verify the outcome, record evidence, and schedule follow-up when recovery is still pending.

A shared upstream component is a diagnostic clue, not proof of root cause. A customer reporting improvement is also an observation rather than automatic proof of durable recovery.

## Capability coverage

| Discipline | Responsibility in this project |
| --- | --- |
| AI and ML basics | Prepare data, build baselines, evaluate classifiers, address imbalance and leakage |
| Deep learning and NLP | Understand neural networks, embeddings, attention, and pretrained model adaptation |
| Prompt engineering | Specify behavior, evidence requirements, clarification, abstention, and structured outputs |
| RAG | Retrieve approved manuals, runbooks, policies, and troubleshooting procedures with references |
| Context engineering | Select relevant case state, history, evidence, tools, timestamps, and execution budgets |
| Loop engineering | Bound cycles of observation, action selection, execution, validation, and termination |
| Graph engineering | Implement diagnostic control flow and network relationship queries |
| Agents | Select permitted investigative steps for ambiguous faults |
| Tool calling | Access operational APIs through typed and authorized interfaces |
| Harness engineering | Supply permissions, budgets, persistence, validation, tracing, recovery, and evaluation |
| Conversational AI | Handle corrections, clarifications, interruptions, resumption, and human handoff |
| STT and TTS | Transcribe speech and generate spoken responses with interruption handling |
| MLOps and LLMOps | Track versions, experiments, releases, quality, drift, latency, and cost |
| ASDLC | Govern the AI system lifecycle and AI-assisted software delivery |

These responsibilities define how the terms are used here. The project covers the requested engineering disciplines without requiring every branch of AI or foundation-model training.

## Business measures

- Verified resolution rate among eligible cases.
- Time to restoration and support handling time.
- Repeat contact and reopened-case rates over an agreed window.
- Unnecessary technician dispatches and appointment corrections.
- Customer satisfaction and quality of human handoffs.
- Total operating cost per verified resolution.

Compare similar fault categories, channels, and customer cohorts. Preserve escalation quality and customer satisfaction when measuring automation gains.

## Production validation

Use de-identified historical data and simulators to establish engineering quality. Validate operational value through a controlled pilot using real integrations, representative users, observed outcomes, and clear support ownership.

Start with a deterministic workflow and one diagnostic agent. Add specialized agents only when a benchmark shows a benefit that exceeds the coordination cost. The distinction between workflows and agents is described in [Anthropic's agent engineering guidance](https://www.anthropic.com/research/building-effective-agents).
