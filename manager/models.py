"""Load all the models to create tables"""
# pylint: disable=unused-imports
from manager.submodels.base_models import (
    Country,
    AttributeCategory,
)
from manager.submodels.user_models import (
    Manager,
    User,
)
from manager.submodels.core_models import (
    PlayerPosition,
    ContractType,
    TransferStatus,
    PlayerStatus,
    OfferStatus,
    OfferType,
    League,
    Team,
    Player,
    Transfer,
    CounterOffer,
    PlayerNegotiation,
    ManagerNegotiation,
)
