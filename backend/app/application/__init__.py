"""Application layer — application-specific business rules (use cases).

Orchestrates the flow of data to and from entities. Depends only on the domain
layer and on the *ports* (abstract interfaces) it defines here; concrete adapters
(databases, hashing, tokens, HTTP) are injected from the outside. Use cases accept
command DTOs and return entities or result DTOs — never framework objects.
"""
