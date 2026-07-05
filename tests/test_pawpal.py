"""Beginner-friendly tests for PawPal+ core logic."""

import os
import sys

# Let this test file find pawpal_system.py in the project's parent folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should set the task's completed flag to True."""
    task = Task("Morning walk", 30, 1, "walk")

    assert task.completed is False  # starts incomplete

    task.mark_complete()

    assert task.completed is True  # now complete


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its number of tasks."""
    pet = Pet("Biscuit", "Dog", 3)

    assert len(pet.get_tasks()) == 0  # no tasks yet

    pet.add_task(Task("Feeding", 10, 1, "feeding"))

    assert len(pet.get_tasks()) == 1  # one task after adding
