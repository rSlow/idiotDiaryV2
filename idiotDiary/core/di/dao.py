from dishka import Scope, provide, Provider, provide_all

from idiotDiary.core.db.dao import DaoHolder
from idiotDiary.core.db.dao.birthday import BirthdayDao
from idiotDiary.core.db.dao.log import EventLogDao
from idiotDiary.core.db.dao.notification import UserNotificationDao
from idiotDiary.core.db.dao.role import RoleDao
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.db.dao.user import UserDao


class DaoProvider(Provider):
    scope = Scope.REQUEST

    holder = provide(DaoHolder)

    dao = provide_all(
        UserDao, EventLogDao, BirthdayDao, UserNotificationDao, RoleDao, SubscriptionDao
    )
