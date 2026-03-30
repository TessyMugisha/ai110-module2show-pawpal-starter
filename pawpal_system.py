from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    description: str
    duration: int  # in minutes
    frequency: str  # e.g. "daily", "weekly", "as needed"
    priority: int = 1  # 1 = high, 2 = medium, 3 = low
    status: str = "pending"  # "pending" or "completed"
    time: Optional[str] = None  # HH:MM optional scheduled time
    last_completed: Optional[date] = None
    pet: Optional["Pet"] = None

    def mark_complete(self, completion_date: Optional[date] = None):
        """Mark this task as completed and track when it was done."""
        self.status = "completed"
        self.last_completed = completion_date or date.today()
        return self.clone_next_occurrence()

    def clone_next_occurrence(self) -> Optional["Task"]:
        """Return a new pending task for the next daily or weekly occurrence."""
        frequency = self.frequency.lower().strip()
        if frequency not in {"daily", "weekly"}:
            return None
        return Task(
            description=self.description,
            duration=self.duration,
            frequency=self.frequency,
            priority=self.priority,
            status="pending",
            time=self.time,
            last_completed=None,
            pet=self.pet,
        )

    def reset(self):
        """Reset this task back to pending and clear completion history."""
        self.status = "pending"
        self.last_completed = None

    def is_complete(self) -> bool:
        """Return True if the task has been completed."""
        return self.status == "completed"

    def is_due(self, plan_date: date) -> bool:
        """Return True if the task should be scheduled for the given date."""
        frequency = self.frequency.lower().replace("_", " ").replace("-", " ")
        if frequency in {"as needed", "as needed"}:
            return not self.is_complete()
        if self.last_completed is None:
            return True
        if frequency == "daily":
            return self.last_completed < plan_date
        if frequency == "weekly":
            return (plan_date - self.last_completed).days >= 7
        return not self.is_complete()


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            task.pet = None
            self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks that have not been completed."""
        return [t for t in self.tasks if not t.is_complete()]

    def get_completed_tasks(self) -> List[Task]:
        """Return all tasks that have been completed."""
        return [t for t in self.tasks if t.is_complete()]

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Return tasks for this pet with the given status."""
        status = status.lower()
        return [t for t in self.tasks if t.status.lower() == status]

    def get_tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Return tasks for this pet with the given frequency."""
        frequency = frequency.lower()
        return [t for t in self.tasks if t.frequency.lower() == frequency]


class Owner:
    def __init__(self, name: str, availability: int = 60, preferences: dict = None):
        self.name = name
        self.availability = availability  # minutes available today
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from this owner's pet list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all pending tasks across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_pending_tasks()]

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Return all tasks across pets that match the given status."""
        status = status.lower()
        return [task for task in self.get_all_tasks() if task.status.lower() == status]

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks assigned to a specific pet."""
        return [task for pet in self.pets if pet.name == pet_name for task in pet.tasks]

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.get_all_tasks()
        if pet_name:
            tasks = [
                task for pet in self.pets if pet.name == pet_name for task in pet.tasks
            ]
        if status:
            status = status.lower()
            tasks = [task for task in tasks if task.status.lower() == status]
        return tasks

    def get_due_tasks(self, plan_date: date) -> List[Task]:
        """Return every task that should be considered on the plan date."""
        return [task for task in self.get_all_tasks() if task.is_due(plan_date)]


class Scheduler:
    def __init__(self, owner: Owner, plan_date: date = None):
        self.owner = owner
        self.plan_date = plan_date or date.today()
        self.scheduled_tasks: List[Task] = []
        self.conflicts: List[str] = []

    def generate_plan(
        self,
        pet_name: Optional[str] = None,
        status_filter: Optional[str] = None,
    ) -> List[Task]:
        """Build a schedule using due tasks, optional filters, and available time."""
        tasks = self.owner.filter_tasks(pet_name=pet_name, status=status_filter)
        tasks = [task for task in tasks if task.is_due(self.plan_date)]

        if any(task.time for task in tasks):
            tasks = self.sort_by_time(tasks)
        else:
            tasks.sort(
                key=lambda task: (task.priority, task.duration, task.description)
            )

        scheduled = []
        time_remaining = self.owner.availability
        for task in tasks:
            if task.duration <= time_remaining:
                scheduled.append(task)
                time_remaining -= task.duration

        self.scheduled_tasks = scheduled
        self.conflicts = self._find_conflicts(tasks)
        return scheduled

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their optional HH:MM time string."""
        return sorted(tasks, key=lambda task: self._time_key(task.time))

    def _time_key(self, time_str: Optional[str]) -> int:
        """Convert an HH:MM string to total minutes; untimed tasks sort last."""
        if not time_str:
            return 24 * 60
        try:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        except ValueError:
            return 24 * 60

    def _find_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for unscheduled tasks and exact-time clashes."""
        messages: List[str] = []

        # Tasks that didn't fit within available time
        unscheduled = [task for task in tasks if task not in self.scheduled_tasks]
        if unscheduled:
            messages.append(
                f"{len(unscheduled)} task(s) could not be scheduled in {self.owner.availability} available minutes."
            )
            for task in unscheduled:
                messages.append(
                    f"- {task.description} ({task.duration} min, {task.frequency})"
                )

        # Tasks scheduled at the same time
        timed = [t for t in self.scheduled_tasks if t.time]
        seen: dict = {}
        for task in timed:
            if task.time in seen:
                other = seen[task.time]
                pet_a = task.pet.name if task.pet else "Unknown"
                pet_b = other.pet.name if other.pet else "Unknown"
                messages.append(
                    f"Time conflict at {task.time}: '{task.description}' ({pet_a})"
                    f" overlaps with '{other.description}' ({pet_b})"
                )
            else:
                seen[task.time] = task

        return messages

    def display_plan(self) -> str:
        """Return a formatted string of today's scheduled tasks."""
        lines = [f"Daily plan for {self.plan_date} — {self.owner.name}"]
        lines.append(f"Available time: {self.owner.availability} minutes\n")
        if not self.scheduled_tasks:
            lines.append("No tasks scheduled.")
        else:
            for task in self.scheduled_tasks:
                lines.append(
                    f"- {task.description} ({task.duration} min, {task.frequency}) [{task.status}]"
                )
        if self.conflicts:
            lines.append("\nUnscheduled tasks due to time or conflicts:")
            lines.extend(self.conflicts)
        return "\n".join(lines)

    def explain_plan(self) -> str:
        """Explain the reasoning behind the generated plan."""
        if not self.scheduled_tasks:
            return "No due tasks fit into the owner's current availability."
        return (
            "Tasks were selected by due date, priority, and shortest duration first. "
            "Only tasks that are due on the plan date were considered. "
            "Remaining due tasks are listed as conflicts when they could not fit."
        )

    def mark_task_complete(self, task: Task, completion_date: Optional[date] = None):
        """Mark a specific task as completed and queue the next occurrence for recurring tasks."""
        next_task = task.mark_complete(completion_date)
        if next_task and task.pet:
            task.pet.add_task(next_task)
        return next_task
