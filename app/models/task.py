from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Instance methods
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "is_complete": self.completed_at is not None
        }
    

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data.get("completed_at", None)  # This will be None if not provided
                    )
        return new_task
