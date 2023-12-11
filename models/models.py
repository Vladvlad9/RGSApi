from datetime import datetime
from typing import Annotated

from sqlalchemy import Boolean, BigInteger, String, DateTime, Integer, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()
#
# intPK = Annotated[int, mapped_column(primary_key=True)]


# class User(Base):
#     __tablename__: str = 'users'
#
#     id: Mapped[intPK]
#     user_id = Column(BigInteger, nullable=False, unique=True, index=True, comment="User ID")
#     phone: Mapped[str] = mapped_column(nullable=False, unique=True, index=True, comment="Phone number")
#     is_active: Mapped[bool] = mapped_column(default=True, comment="Is the user active?")
#     created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, comment="Creation timestamp")
#     updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow,
#                                                  comment="Last update timestamp")

class User(Base):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, unique=True, index=True, comment="User ID")
    phone = Column(String, nullable=False, comment="User ID")
    is_block = Column(Boolean, default=True, nullable=False, comment="Is the user active?")

    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="Last update timestamp")


class Admin(Base):
    __tablename__: str = "admins"

    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger, nullable=False, unique=True, index=True)


class Dialogue(Base):
    __tablename__: str = "dialogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    admin_id = Column(BigInteger, index=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, comment="Creation timestamp")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Last update timestamp")
    who_closed = Column(String, default="None")
    gradeUser = Column(Integer)
    gradeAdmin = Column(Integer)


class TelegramMessage(Base):
    __tablename__ = 'telegram_message'

    id = Column(Integer, primary_key=True)


class AdminWebs(Base):
    __tablename__ = 'admin_webs'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
