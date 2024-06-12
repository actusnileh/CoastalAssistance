from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, BigInteger
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(Text, nullable=True)
    usertype = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)

    shores = relationship("Shore", back_populates="user", cascade="all, delete-orphan")


class Shore(Base):
    __tablename__ = "shores"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    photo = Column(Text, nullable=True)
    geo_tag = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    destruction = Column(BigInteger, nullable=False)
    activated = Column(BigInteger, nullable=False)

    user = relationship("User", back_populates="shores")
