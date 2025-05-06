from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Instance methods
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "is_complete": True if self.completed_at else False
        }
    

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data.get("completed_at")  # This will be None if not provided
                        )
        return new_task
