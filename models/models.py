from datetime import datetime

from sqlalchemy import Boolean, BigInteger, String, DateTime, Integer, Column, Date, ForeignKey, SMALLINT, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def get_current_time():
    return datetime.utcnow()


class User(Base):
    __tablename__: str = 'users'

    # id = Column(Integer, autoincrement=True, unique=True)
    # user_id = Column(BigInteger, primary_key=True)
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)

    last_name = Column(String, default="None", comment="Last name", unique=True)
    first_name = Column(String, default="None", comment="First name", unique=True)
    middle_name = Column(String, default="None", comment="Middle name", unique=True)

    lnr = Column(String, comment="number LNR", unique=True)

    phone = Column(String, comment="User phone number", unique=True)
    is_block = Column(Boolean, comment="Is the user active?")
    quotation_number = Column(String, unique=True)
    created_at = Column(DateTime, comment="Creation timestamp")
    updated_at = Column(DateTime, onupdate=datetime.now, comment="Last update timestamp")

    sales_channel_id = Column(
        SMALLINT,
        ForeignKey("sales_channel.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    sales_channel = relationship("SalesChannel",
                                 back_populates="users", cascade="all, delete-orphan", single_parent=True)

    dialogue = relationship("Dialogue", back_populates="user", foreign_keys="Dialogue.user_id")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class Admin(Base):
    __tablename__: str = "admins"

    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger, unique=True)

    last_name = Column(String, default="None", comment="Last name")
    first_name = Column(String, default="None", comment="First name")
    middle_name = Column(String, default="None", comment="Middle name")

    groups_id = Column(Integer, ForeignKey("groups.id"))

    groups = relationship("Groups", back_populates="admin_groups")
    dialogue = relationship("Dialogue", back_populates="admin", foreign_keys="Dialogue.admin_id")

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
        ForeignKey("users.id", onupdate="CASCADE"),
    )
    admin_id = Column(
        BigInteger,
        ForeignKey("admins.id", onupdate="CASCADE"),
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

    user = relationship(
        "User",
        back_populates="dialogue",
    )
    admin = relationship(
        "Admin",
        back_populates="dialogue",
    )

    def __str__(self):
        return f"Диалог №{self.id}"


class SalesChannel(Base):
    __tablename__ = 'sales_channel'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship("User", back_populates="sales_channel")

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