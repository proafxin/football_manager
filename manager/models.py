"""Load all the models to create tables."""

from manager.submodels.base_models import Country  # noqa: F401
from manager.submodels.core_models import (
    AttributeCategory,  # noqa: F401
    CounterOffer,  # noqa: F401
    League,  # noqa: F401
    ManagerNegotiation,  # noqa: F401
    Player,  # noqa: F401
    PlayerNegotiation,  # noqa: F401
    Team,  # noqa: F401
    Transfer,  # noqa: F401
)
from manager.submodels.user_models import Manager, User  # noqa: F401
