from datetime import datetime
from typing import Annotated

from sqlalchemy import Boolean, BigInteger, String, DateTime, Integer, Column, ForeignKey, SMALLINT, Float
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
    user_id = Column(BigInteger, unique=True, index=True, comment="User ID")

    last_name = Column(String, comment="Last name")
    first_name = Column(String, comment="First name")
    middle_name = Column(String, comment="Middle name")

    lnr = Column(String, comment="number LNR")

    phone = Column(String, comment="User phone number")
    is_block = Column(Boolean, comment="Is the user active?")
    quotation_number = Column(String)
    created_at = Column(DateTime, comment="Creation timestamp")
    updated_at = Column(DateTime, onupdate=datetime.now, comment="Last update timestamp")

    groups_id = Column(
        SMALLINT,
        ForeignKey(column="groups.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    groups = relationship("Groups", back_populates="user_groups")
    dialogue = relationship("Dialogue", back_populates="user")

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
    dialogue = relationship("Dialogue", back_populates="admin", cascade="all, delete-orphan", single_parent=True)

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
    user_id = Column(
        BigInteger,
        ForeignKey(column="users.user_id", ondelete="RESTRICT", onupdate="CASCADE"),
    )
    admin_id = Column(
        BigInteger,
        ForeignKey(column="admins.admin_id", ondelete="RESTRICT", onupdate="CASCADE"),
    )
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now,
                        comment="Last update timestamp")
    who_closed = Column(String, default="None")
    gradeUser = Column(Integer)
    gradeAdmin = Column(Integer)
    chat_name = Column(String)

    dialogue_time = Column(Float)
    reaction_time = Column(Float)

    sales_channel_id = Column(
        SMALLINT,
        ForeignKey(column="sales_channel.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    sales_channel = relationship("SalesChannel",
                                 back_populates="dialogue", cascade="all, delete-orphan", single_parent=True)

    user = relationship("User", back_populates="dialogue", cascade="all, delete-orphan", single_parent=True)
    admin = relationship("Admin", back_populates="dialogue", cascade="all, delete-orphan", single_parent=True)

    def __str__(self):
        return f"Диалог №{self.id}"


class SalesChannel(Base):
    __tablename__ = 'sales_channel'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    dialogue = relationship("Dialogue", back_populates="sales_channel")

    def __str__(self):
        return self.name


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_groups = relationship("User", back_populates="groups")
    admin_groups = relationship("Admin", back_populates="groups")

    def __str__(self):
        return self.name


class TelegramMessage(Base):
    __tablename__ = 'telegram_message'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now, comment="Creation timestamp")
    forWhom = Column(String)
    countMessageAdmin = Column(Integer)
    message = Column(String)
