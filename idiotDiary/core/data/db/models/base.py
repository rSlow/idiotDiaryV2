from typing import Mapping

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

convention: Mapping[str, str] = {
    # "pk": "pk__%(table_name)s",
}
meta = MetaData(naming_convention=convention)  # TODO naming_convention


class Base(DeclarativeBase):
    metadata = meta
