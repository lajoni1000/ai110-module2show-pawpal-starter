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
        print(
            f"  {i}. {task.description:<20} "
            f"{task.duration:>3} min  "
            f"[{priority:<6}] "
            f"{task.task_type}"
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

    dog.add_task(Task("Morning walk", 30, 1, "walk"))
    dog.add_task(Task("Grooming", 45, 3, "grooming"))
    cat.add_task(Task("Feeding", 10, 1, "feeding"))
    cat.add_task(Task("Medication", 15, 2, "medication"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    print_schedule(daily_plan, owner.available_time)


if __name__ == "__main__":
    main()