from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    This class serves as the declarative base used to define all database
    models in the application. All ORM models should inherit from this class
    to ensure proper metadata registration and schema generation.
    """

    pass
