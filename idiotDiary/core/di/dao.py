from dishka import Scope, provide, Provider

from idiotDiary.core.db.dao import DaoHolder
from idiotDiary.core.db.dao.birthday import BirthdayDao
from idiotDiary.core.db.dao.log import EventLogDao
from idiotDiary.core.db.dao.notification import UserNotificationDao
from idiotDiary.core.db.dao.role import RoleDao
from idiotDiary.core.db.dao.user import UserDao


class DaoProvider(Provider):
    scope = Scope.REQUEST

    dao = provide(DaoHolder)
    user_dao = provide(UserDao)
    log_dao = provide(EventLogDao)
    birthday_dao = provide(BirthdayDao)
    notifications_dao = provide(UserNotificationDao)
    role_dao = provide(RoleDao)
