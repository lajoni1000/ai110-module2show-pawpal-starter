from pawpal_system import Owner, Pet, Task, Scheduler


PRIORITY_LABELS = {1: "High", 2: "Medium", 3: "Low"}


def print_schedule(tasks, available_time=None):
    """Print the daily schedule in a readable, aligned format."""
    print("\nToday's PawPal+ Schedule")
    print("=" * 44)

    if not tasks:
        print("  No tasks scheduled today.")
        print("=" * 44)
        return

    for i, task in enumerate(tasks, start=1):
        priority = PRIORITY_LABELS.get(task.priority, f"P{task.priority}")
        status = "done" if task.completed else "todo"
        print(
            f"  {i}. {task.time}  {task.description:<20} "
            f"{task.duration:>3} min  "
            f"[{priority:<6}] "
            f"{task.task_type:<10} ({status})"
        )

    print("-" * 44)
    total = sum(task.duration for task in tasks)
    if available_time is not None:
        print(f"  Total: {total} of {available_time} min used "
              f"({available_time - total} min free)")
    else:
        print(f"  Total: {total} min")
    print("=" * 44)


def main():
    owner = Owner(
        name="Hanny",
        available_time=60,
        preferences=["morning walks", "high priority tasks first"],
    )

    dog = Pet(name="Biscuit", species="Dog", age=3)
    cat = Pet(name="Mochi", species="Cat", age=2)

    # Added out of chronological order on purpose, to prove sort_by_time works.
    dog.add_task(Task("Grooming", 45, 3, "grooming", time="16:00", recurrence="weekly"))
    dog.add_task(Task("Morning walk", 30, 1, "walk", time="07:30", recurrence="daily"))
    cat.add_task(Task("Medication", 15, 2, "medication", time="12:15"))
    cat.add_task(Task("Feeding", 10, 1, "feeding", time="06:45", recurrence="daily"))
    # Scheduled at 07:30 — the SAME time as Biscuit's Morning walk, to trigger
    # a cross-pet conflict warning.
    cat.add_task(Task("Litter box cleaning", 10, 2, "cleaning", time="07:30"))

    # Mark one task done so the status filter has something to hide.
    cat.tasks[0].mark_complete()  # Medication (one-off, no next occurrence)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    # 1. Sorting by time — note the tasks come back in chronological order
    #    even though they were added out of order above.
    print("\n--- All tasks sorted by time ---")
    all_tasks = owner.get_all_tasks()
    print_schedule(scheduler.sort_by_time(all_tasks))

    # 2. Filtering by pet name
    print("\n--- Biscuit's tasks only (sorted by time) ---")
    biscuit_tasks = scheduler.filter_by(pet_name="Biscuit")
    print_schedule(scheduler.sort_by_time(biscuit_tasks))

    # 3. Filtering by completion status (only unfinished tasks)
    print("\n--- Unfinished tasks only (sorted by time) ---")
    todo_tasks = scheduler.filter_by(completed=False)
    print_schedule(scheduler.sort_by_time(todo_tasks))

    # 4. Conflict detection — two tasks scheduled at the same time.
    print("\n--- Conflict detection ---")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("  No scheduling conflicts. ")

    # 5. Recurring tasks — completing a daily/weekly task auto-schedules the next one.
    print("\n--- Recurring tasks ---")
    walk = dog.get_tasks()[1]  # Morning walk, recurrence="daily"
    print(f"Before: Biscuit has {len(dog.get_tasks())} task(s).")
    next_walk = dog.complete_task(walk)
    print(
        f"Completed '{walk.description}' (due {walk.due_date}). "
        f"Auto-created next '{next_walk.description}' due {next_walk.due_date}."
    )
    print(f"After:  Biscuit has {len(dog.get_tasks())} task(s).")

    # Original priority-based daily plan, still working as before.
    daily_plan = scheduler.generate_daily_plan()
    print_schedule(daily_plan, owner.available_time)


if __name__ == "__main__":
    main()