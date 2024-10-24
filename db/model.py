from sqlalchemy import BIGINT, TEXT, ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import AbstractClass


class User(AbstractClass):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50))

    customers: Mapped[list['Customer']] = relationship(back_populates="user")
    freelancers: Mapped[list['Freelancer']] = relationship(back_populates="user")


class Customer(AbstractClass):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    lang: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(13))
    role: Mapped[str] = mapped_column(default="CUSTOMER")

    user: Mapped['User'] = relationship(back_populates="customers")
    tasks: Mapped[list['Task']] = relationship(back_populates='customer')


class Freelancer(AbstractClass):
    __tablename__ = "freelancers"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    lang: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(13))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    role: Mapped[str] = mapped_column(default="FREELANCER")

    user: Mapped['User'] = relationship(back_populates="freelancers")
    category: Mapped['Category'] = relationship(back_populates="freelancers")


class Category(AbstractClass):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()

    tasks: Mapped[list['Task']] = relationship(back_populates="category")
    freelancers: Mapped[list['Freelancer']] = relationship(back_populates="category")


class Task(AbstractClass):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(TEXT)
    status: Mapped[str] = mapped_column(default="PROCESSING")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped['Category'] = relationship(back_populates="tasks")
    customer: Mapped['Customer'] = relationship(back_populates="tasks")
