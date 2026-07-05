"""PawPal+ core domain classes.

Implemented from diagrams/uml_draft.mmd.
Task and Pet are dataclasses; Owner and Scheduler are behavior-oriented classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations


@dataclass
class Task:
    """A single pet care task (e.g., a walk, feeding, or medication)."""

    description: str
    duration: int
    priority: int
    task_type: str
    completed: bool = False
    time: str = "00:00"  # scheduled start time, "HH:MM" 24-hour format
    recurrence: str = "none"  # "none", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)

    def next_occurrence(self) -> "Task | None":
        """Return a fresh, uncompleted copy for this task's next due date.

        Uses ``timedelta`` to advance ``due_date`` by one day ("daily") or one
        week ("weekly").

        Returns:
            A new ``Task`` (not completed) whose ``due_date`` is advanced by the
            recurrence interval, copying all other fields. Returns ``None`` for
            non-recurring tasks, so callers can tell there is nothing to
            schedule again.
        """
        if self.recurrence == "daily":
            delta = timedelta(days=1)
        elif self.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            duration=self.duration,
            priority=self.priority,
            task_type=self.task_type,
            completed=False,
            time=self.time,
            recurrence=self.recurrence,
            due_date=self.due_date + delta,
        )

    def mark_complete(self) -> "Task | None":
        """Mark this task complete and return its next occurrence, if any.

        Returns the newly created follow-up ``Task`` for recurring tasks, or
        ``None`` for one-off tasks.
        """
        self.completed = True
        return self.next_occurrence()


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

    def complete_task(self, task: Task) -> Task | None:
        """Mark one of this pet's tasks complete, auto-scheduling any recurrence.

        Delegates to ``task.mark_complete()``; if that returns a next occurrence
        (for daily/weekly tasks), it is appended to this pet's task list so the
        follow-up is scheduled automatically. Returns the new task, or ``None``.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


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

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically by their ``time`` ("HH:MM").

        Uses a lambda ``key`` that converts each "HH:MM" string into an
        ``(hour, minute)`` tuple of ints. Sorting on that tuple is robust even
        if a time is not zero-padded (e.g. "9:30"), which a plain string sort
        would order incorrectly.
        """
        return sorted(
            tasks,
            key=lambda task: (
                int(task.time.split(":")[0]),
                int(task.time.split(":")[1]),
            ),
        )

    @staticmethod
    def _to_minutes(time_str: str) -> int | None:
        """Convert an "HH:MM" string to minutes since midnight, or None if invalid.

        Returns ``None`` instead of raising so a malformed time never crashes
        conflict detection (the "lightweight, don't crash" requirement).
        """
        try:
            hours, minutes = time_str.split(":")
            return int(hours) * 60 + int(minutes)
        except (ValueError, AttributeError):
            return None

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks whose scheduled times overlap.

        Two tasks conflict when they share a ``due_date`` and their time
        intervals ``[start, start + duration)`` overlap. Works within a single
        pet and across different pets. Completed tasks and tasks with an
        unparseable ``time`` are skipped. Returns an empty list when there are
        no conflicts (never raises).
        """
        entries = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if task.completed:
                    continue
                start = self._to_minutes(task.time)
                if start is None:
                    continue
                entries.append((pet, task, start, start + task.duration))

        warnings: list[str] = []
        for (pet_a, task_a, start_a, end_a), (pet_b, task_b, start_b, end_b) in combinations(entries, 2):
            same_day = task_a.due_date == task_b.due_date
            overlaps = start_a < end_b and start_b < end_a
            if same_day and overlaps:
                warnings.append(
                    f"[!] Conflict: '{task_a.description}' "
                    f"({pet_a.name}, {task_a.time}, {task_a.duration} min) "
                    f"overlaps '{task_b.description}' "
                    f"({pet_b.name}, {task_b.time}, {task_b.duration} min)"
                )
        return warnings

    def filter_by(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks matching the given completion status and/or pet name.

        Walks the owner's pets so tasks can be matched to their pet. Any filter
        left as ``None`` is ignored, so ``filter_by()`` returns every task,
        ``filter_by(completed=False)`` returns only unfinished tasks, and
        ``filter_by(pet_name="Mochi")`` returns only that pet's tasks.
        """
        result: list[Task] = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                result.append(task)
        return result

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
