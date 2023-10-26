from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для пожертвований."""


donation_crud = CRUDDonation(Donation)
