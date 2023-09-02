from app.models import LoginHistoryCreate, LoginHistoryDB, LoginHistoryUpdate

from .crudbase import CRUDBase


class CRUDLoginHistory(
    CRUDBase[LoginHistoryDB, LoginHistoryCreate, LoginHistoryUpdate]
):
    pass


login_history = CRUDLoginHistory(LoginHistoryDB)
