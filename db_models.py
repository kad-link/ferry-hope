from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, ForeignKey, func


class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Order(Base):

    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    ordered_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    placed_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped[list["User"]] = relationship(back_populates="orders")


class Product(Base):

    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
