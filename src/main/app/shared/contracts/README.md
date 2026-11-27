# Shared contracts

Framework-independent request, response, event, and context contracts shared across service boundaries. Keep one contract class per file. Contracts must not import services, providers, repositories, or business implementations.

`RequestContext` carries identifiers established by trusted upstream verification. Constructing it validates shape only; it does not authenticate a customer or authorize an action. Each operational adapter must enforce access before reading or writing data.
