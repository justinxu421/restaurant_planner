from .base import Base  # noqa

# Import all the models, so that the Base class 
# has them before being imported by Alembic.
from .. import models # noqa