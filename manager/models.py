"""Load all the models to create tables"""
# pylint: disable=unused-imports
from manager.submodels.base_models import Country
from manager.submodels.core_models import (
    AttributeCategory,
    ContractType,
    CounterOffer,
    League,
    ManagerNegotiation,
    OfferStatus,
    OfferType,
    Player,
    PlayerNegotiation,
    PlayerPosition,
    PlayerStatus,
    Team,
    Transfer,
    TransferStatus,
)
from manager.submodels.user_models import (
    Manager,
    User,
)
