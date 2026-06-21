"""Infrastructure layer — frameworks, drivers, and interface adapters to the outside.

The outermost circle. Concrete implementations of the ports defined in the
application layer: SQLAlchemy persistence, bcrypt hashing, JWT tokens, settings.
These are details — plugins to the business rules, not the other way around.
"""
