"""PawPal+ core domain classes.

Class skeletons generated from diagrams/uml_draft.mmd.
Business logic is intentionally left unimplemented (method stubs only).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task (e.g., a walk, feeding, or medication)."""

    description: str
    duration: int
    priority: int
    task_type: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    """A pet that belongs to an owner and has a list of care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass


class Owner:
    """A pet owner with time constraints, preferences, and one or more pets."""

    def __init__(
        self,
        name: str,
        available_time: int,
        preferences: list | None = None,
        pets: list[Pet] | None = None,
    ) -> None:
        """Initialize an owner with basic info, preferences, and pets."""
        self.name = name
        self.available_time = available_time
        self.preferences = preferences if preferences is not None else []
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across every pet this owner has."""
        pass


class Scheduler:
    """Builds a daily plan for an owner by sorting and filtering their tasks."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler for a given owner."""
        self.owner = owner

    def generate_daily_plan(self) -> list[Task]:
        """Produce an ordered daily plan of tasks based on constraints."""
        pass

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority (lower number = higher priority)."""
        pass

    def filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return only the tasks that fit the owner's available time."""
        pass
