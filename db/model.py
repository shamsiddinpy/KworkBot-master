from sqlalchemy import BIGINT, TEXT, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import AbstractClass


class Customer(AbstractClass):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT)
    lang: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(13))
    role: Mapped[str] = mapped_column(default="CUSTOMER")
    tasks: Mapped[list['Task']] = relationship(back_populates='customer')


class Freelancer(AbstractClass):
    __tablename__ = "freelancers"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT)
    lang: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(13))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    role: Mapped[str] = mapped_column(default="FREELANCER")
    category: Mapped['Category'] = relationship(back_populates="freelancers")


class Category(AbstractClass):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()
    tasks: Mapped[list['Task']] = relationship(back_populates="category")
    freelancers: Mapped[list['Freelancer']] = relationship(back_populates="category")


#
class Task(AbstractClass):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(TEXT)
    status: Mapped[str] = mapped_column(default="PROCESSING")
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped['Category'] = relationship(back_populates="tasks")
    customer: Mapped['Customer'] = relationship(back_populates="tasks")


class ShUser(AbstractClass):
    __tablename__ = "sh_users"
    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
