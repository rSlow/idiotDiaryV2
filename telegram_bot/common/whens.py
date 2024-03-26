from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from config import settings
from .types import UserIDType


class WhenUserID:
    def __init__(self, users_id: UserIDType):

        if not isinstance(users_id, list | tuple):
            users_id = (users_id,)
        self.users_id = users_id

    def __call__(self,
                 _: dict,
                 __: Whenable,
                 manager: DialogManager):
        user: User = manager.middleware_data["event_from_user"]
        user_id = user.id
        if str(user_id) in self.users_id:
            return True
        return False


class WhenOwner(WhenUserID):
    def __init__(self):
        super().__init__(settings.OWNER_ID)


class WhenBirthdays(WhenUserID):
    def __init__(self):
        super().__init__(settings.BIRTHDAYS_ALLOWED)
