from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.base_model import DateTimeMixin, Base


class Dish(Base, DateTimeMixin):
    __tablename__ = "dishs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
