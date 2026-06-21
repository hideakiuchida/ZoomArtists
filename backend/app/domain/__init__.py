"""Domain layer — enterprise business rules.

The innermost circle. Contains pure entities, value objects, and domain errors.
Nothing here may import from application, infrastructure, api, or any framework
(no FastAPI, SQLAlchemy, Pydantic). Dependencies point *inward* toward this layer.
"""
