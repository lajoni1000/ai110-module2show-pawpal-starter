"""Beginner-friendly tests for PawPal+ core logic.

Run from the project folder with:  pytest -v

The tests are grouped by feature (sorting, filtering, recurrence, conflicts).
Each test name says what it checks, and comments explain the "why".
"""

import os
import sys
from datetime import date, timedelta

import pytest

# Let this test file find pawpal_system.py in the project's parent folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Owner, Pet, Scheduler, Task


# ---------------------------------------------------------------------------
# Fixtures: small reusable helpers so we don't rebuild the same objects
# in every test. A function marked with @pytest.fixture can be requested
# by any test just by naming it as an argument.
# ---------------------------------------------------------------------------

# A fixed date so recurrence/conflict tests never depend on "today".
FIXED_DAY = date(2026, 1, 1)


@pytest.fixture
def owner_with_pet():
    """An owner with 60 minutes free and one empty pet named 'Mochi'."""
    pet = Pet("Mochi", "Cat", 2)
    owner = Owner("Alex", available_time=60)
    owner.add_pet(pet)
    # We return both so a test can grab whichever it needs.
    return owner, pet


# ===========================================================================
# 1. BASIC BEHAVIOR (kept from the starter file)
# ===========================================================================

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


# ===========================================================================
# 2. SORTING CORRECTNESS
# ===========================================================================

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order tasks earliest-to-latest by their time."""
    owner = Owner("Alex", available_time=60)
    scheduler = Scheduler(owner)

    # Deliberately out of order in the input list.
    afternoon = Task("Vet call", 15, 2, "admin", time="14:30")
    morning = Task("Breakfast", 10, 1, "feeding", time="08:00")
    noon = Task("Midday walk", 20, 1, "walk", time="12:00")

    result = scheduler.sort_by_time([afternoon, morning, noon])

    # We check the ORDER by pulling the time out of each returned task.
    times_in_order = [task.time for task in result]
    assert times_in_order == ["08:00", "12:00", "14:30"]


def test_sort_by_time_handles_non_padded_hours():
    """'9:30' must come BEFORE '10:00'.

    A plain string sort would put "10:00" first because "1" < "9" as text.
    sort_by_time() converts to (hour, minute) numbers, so 9 < 10 wins.
    This test proves that conversion works.
    """
    owner = Owner("Alex", available_time=60)
    scheduler = Scheduler(owner)

    ten = Task("Later", 10, 1, "walk", time="10:00")
    nine_thirty = Task("Earlier", 10, 1, "walk", time="9:30")

    result = scheduler.sort_by_time([ten, nine_thirty])

    assert [t.time for t in result] == ["9:30", "10:00"]


def test_sort_tasks_orders_by_priority():
    """sort_tasks() should put lower priority numbers first (1 = most urgent)."""
    owner = Owner("Alex", available_time=60)
    scheduler = Scheduler(owner)

    low = Task("Brush", 5, 3, "grooming")
    high = Task("Medication", 5, 1, "meds")

    result = scheduler.sort_tasks([low, high])

    assert [t.priority for t in result] == [1, 3]


def test_sort_by_time_empty_list_returns_empty():
    """Sorting an empty list should just give back an empty list (no crash)."""
    scheduler = Scheduler(Owner("Alex", 60))
    assert scheduler.sort_by_time([]) == []


# ===========================================================================
# 3. FILTERING
# ===========================================================================

def test_filter_by_no_arguments_returns_all_tasks(owner_with_pet):
    """filter_by() with no filters returns every task the owner has."""
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 20, 1, "walk"))
    pet.add_task(Task("Feed", 10, 1, "feeding"))

    scheduler = Scheduler(owner)
    assert len(scheduler.filter_by()) == 2


def test_filter_by_completed_false_hides_finished_tasks(owner_with_pet):
    """filter_by(completed=False) should return only unfinished tasks."""
    owner, pet = owner_with_pet
    done = Task("Walk", 20, 1, "walk")
    done.mark_complete()  # this one is finished
    pet.add_task(done)
    pet.add_task(Task("Feed", 10, 1, "feeding"))  # this one is not

    scheduler = Scheduler(owner)
    unfinished = scheduler.filter_by(completed=False)

    assert len(unfinished) == 1
    assert unfinished[0].description == "Feed"


def test_filter_by_unknown_pet_name_returns_empty(owner_with_pet):
    """Asking for a pet that doesn't exist returns an empty list, not an error."""
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 20, 1, "walk"))

    scheduler = Scheduler(owner)
    assert scheduler.filter_by(pet_name="Ghost") == []


def test_filter_tasks_keeps_only_what_fits_in_available_time():
    """filter_tasks() greedily keeps tasks until the time budget runs out."""
    owner = Owner("Alex", available_time=30)
    scheduler = Scheduler(owner)

    tasks = [
        Task("A", 20, 1, "walk"),
        Task("B", 20, 1, "walk"),  # 20 + 20 = 40 > 30, so B should be dropped
    ]

    plan = scheduler.filter_tasks(tasks)

    assert [t.description for t in plan] == ["A"]


def test_filter_tasks_includes_exact_fit():
    """A task that fits EXACTLY into the remaining time is kept (uses <=)."""
    owner = Owner("Alex", available_time=30)
    scheduler = Scheduler(owner)

    tasks = [Task("A", 10, 1, "walk"), Task("B", 20, 1, "walk")]  # 10 + 20 = 30

    plan = scheduler.filter_tasks(tasks)

    assert len(plan) == 2  # both fit, since 30 <= 30


# ===========================================================================
# 4. RECURRENCE LOGIC
# ===========================================================================

def test_marking_daily_task_complete_creates_task_for_next_day():
    """A daily task, when completed, should produce a follow-up due tomorrow."""
    task = Task(
        "Morning walk", 30, 1, "walk",
        recurrence="daily",
        due_date=FIXED_DAY,
    )

    next_task = task.mark_complete()

    # A new task was returned (not None)...
    assert next_task is not None
    # ...due exactly one day later...
    assert next_task.due_date == FIXED_DAY + timedelta(days=1)
    # ...and it starts life NOT completed, so it can be done again.
    assert next_task.completed is False
    # The original stays completed.
    assert task.completed is True


def test_weekly_task_advances_by_seven_days():
    """A weekly task's follow-up should be due 7 days later."""
    task = Task("Bath", 45, 2, "grooming", recurrence="weekly", due_date=FIXED_DAY)

    next_task = task.next_occurrence()

    assert next_task.due_date == FIXED_DAY + timedelta(weeks=1)


def test_non_recurring_task_has_no_next_occurrence():
    """A one-off task (recurrence='none') returns None; nothing to reschedule."""
    task = Task("Vet visit", 60, 1, "admin")  # recurrence defaults to "none"

    assert task.next_occurrence() is None
    assert task.mark_complete() is None


def test_complete_task_auto_schedules_recurrence_on_pet(owner_with_pet):
    """pet.complete_task() on a daily task should append the follow-up to the pet."""
    owner, pet = owner_with_pet
    task = Task("Feed", 10, 1, "feeding", recurrence="daily", due_date=FIXED_DAY)
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1

    pet.complete_task(task)

    # The pet now has the original (completed) plus the new follow-up.
    assert len(pet.get_tasks()) == 2


# ===========================================================================
# 5. CONFLICT DETECTION
# ===========================================================================

def test_detect_conflicts_flags_duplicate_times(owner_with_pet):
    """Two tasks at the SAME time on the same day should be flagged as a conflict."""
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 30, 1, "walk", time="09:00", due_date=FIXED_DAY))
    pet.add_task(Task("Feed", 15, 1, "feeding", time="09:00", due_date=FIXED_DAY))

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1  # exactly one clash reported


def test_no_conflict_for_back_to_back_tasks(owner_with_pet):
    """A task ending at 09:30 and one starting at 09:30 do NOT overlap.

    The code treats time as [start, start + duration) -- the end minute is not
    included -- so touching tasks are fine.
    """
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 30, 1, "walk", time="09:00", due_date=FIXED_DAY))
    pet.add_task(Task("Feed", 15, 1, "feeding", time="09:30", due_date=FIXED_DAY))

    assert Scheduler(owner).detect_conflicts() == []


def test_no_conflict_on_different_days(owner_with_pet):
    """Same time but different due_date is not a conflict."""
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 30, 1, "walk", time="09:00", due_date=FIXED_DAY))
    pet.add_task(
        Task("Feed", 30, 1, "feeding", time="09:00",
             due_date=FIXED_DAY + timedelta(days=1))
    )

    assert Scheduler(owner).detect_conflicts() == []


def test_completed_task_is_ignored_in_conflicts(owner_with_pet):
    """A completed task should not create a conflict, even at the same time."""
    owner, pet = owner_with_pet
    done = Task("Walk", 30, 1, "walk", time="09:00", due_date=FIXED_DAY)
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task("Feed", 15, 1, "feeding", time="09:00", due_date=FIXED_DAY))

    assert Scheduler(owner).detect_conflicts() == []


def test_invalid_time_does_not_crash_conflict_detection(owner_with_pet):
    """A task with a garbage time is skipped; detection still returns cleanly."""
    owner, pet = owner_with_pet
    pet.add_task(Task("Walk", 30, 1, "walk", time="banana", due_date=FIXED_DAY))
    pet.add_task(Task("Feed", 15, 1, "feeding", time="09:00", due_date=FIXED_DAY))

    # No exception, and no conflict (the bad-time task can't be compared).
    assert Scheduler(owner).detect_conflicts() == []


def test_conflict_detected_across_different_pets():
    """Overlapping tasks on TWO different pets should still be flagged."""
    owner = Owner("Alex", available_time=60)
    cat = Pet("Mochi", "Cat", 2)
    dog = Pet("Biscuit", "Dog", 3)
    cat.add_task(Task("Cat feed", 30, 1, "feeding", time="09:00", due_date=FIXED_DAY))
    dog.add_task(Task("Dog walk", 30, 1, "walk", time="09:15", due_date=FIXED_DAY))
    owner.add_pet(cat)
    owner.add_pet(dog)

    assert len(Scheduler(owner).detect_conflicts()) == 1
