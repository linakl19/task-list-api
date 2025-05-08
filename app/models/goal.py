from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")


    def to_dict(self):
        goal_dict = {
            "id": self.id,
            "title": self.title,
            # "tasks": [task.to_dict() for task in self.tasks]
        }
        
        if self.tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]
        
        return goal_dict
    

    @classmethod
    def from_dict(cls, goal_data):
        new_goal= cls(title=goal_data["title"])

        return new_goal
