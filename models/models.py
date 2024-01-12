from datetime import datetime
from typing import Annotated

from sqlalchemy import Boolean, BigInteger, String, DateTime, Integer, Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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

    last_name = Column(String, default="None", comment="Last name")
    first_name = Column(String, default="None", comment="First name")
    middle_name = Column(String, default="None", comment="Middle name")

    lnr = Column(String, default="None", comment="number LNR")

    phone = Column(String, nullable=False, comment="User phone number")
    is_block = Column(Boolean, default=True, nullable=False, comment="Is the user active?")

    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="Last update timestamp")

    sales_channel_id = Column(Integer, ForeignKey("sales_channel.id"))
    sales_channel = relationship("SalesChannel", back_populates="user_chanel")


    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class Admin(Base):
    __tablename__: str = "admins"

    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger, nullable=False, unique=True, index=True)

    last_name = Column(String, default="None", comment="Last name")
    first_name = Column(String, default="None", comment="First name")
    middle_name = Column(String, default="None", comment="Middle name")

    groups_id = Column(Integer, ForeignKey("groups.id"))
    groups = relationship("Groups", back_populates="admin_groups")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class AdminWeb(Base):
    __tablename__: str = "admin_webs"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)


class Dialogue(Base):
    __tablename__: str = "dialogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    admin_id = Column(BigInteger, index=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now,
                        comment="Last update timestamp")
    who_closed = Column(String, default="None")
    gradeUser = Column(Integer)
    gradeAdmin = Column(Integer)
    chat_name = Column(String)


    def __str__(self):
        return f"Диалог №{self.id}"


class SalesChannel(Base):
    __tablename__ = 'sales_channel'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_chanel = relationship("User", back_populates="sales_channel")

    def __str__(self):
        return self.name


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    admin_groups = relationship("Admin", back_populates="groups")

    def __str__(self):
        return self.name


class TelegramMessage(Base):
    __tablename__ = 'telegram_message'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    forWhom = Column(String, default="Продавцы")
    countMessageAdmin = Column(Integer)
    message = Column(String)
