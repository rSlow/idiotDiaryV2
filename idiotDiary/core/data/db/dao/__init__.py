from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .log import EventLogDao
from .user import UserDao
from .birthday import BirthdayDao


class DaoHolder:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

        self.user: UserDao = UserDao(self.session)
        self.log: EventLogDao = EventLogDao(self.session)

        self.birthdays: BirthdayDao = BirthdayDao(self.session)
