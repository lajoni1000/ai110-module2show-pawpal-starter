"""PawPal+ core domain classes.

Implemented from diagrams/uml_draft.mmd.
Task and Pet are dataclasses; Owner and Scheduler are behavior-oriented classes.
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
        self.completed = True


@dataclass
class Pet:
    """A pet that belongs to an owner and has a list of care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list (no error if absent)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks


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
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all of this owner's pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Builds a daily plan for an owner by sorting and filtering their tasks."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler for a given owner."""
        self.owner = owner

    def generate_daily_plan(self) -> list[Task]:
        """Produce an ordered daily plan of tasks that fits the owner's time.

        Gathers every pet's tasks, sorts them by priority, then keeps only
        the tasks that fit within the owner's available time.
        """
        tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_tasks(tasks)
        return self.filter_tasks(sorted_tasks)

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority (lower number = higher priority)."""
        return sorted(tasks, key=lambda task: task.priority)

    def filter_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return the incomplete tasks that fit the owner's available time.

        Iterates in the given order and greedily adds tasks while the running
        total stays within ``owner.available_time``. Completed tasks are skipped.
        """
        plan: list[Task] = []
        time_used = 0
        for task in tasks:
            if task.completed:
                continue
            if time_used + task.duration <= self.owner.available_time:
                plan.append(task)
                time_used += task.duration
        return plan
