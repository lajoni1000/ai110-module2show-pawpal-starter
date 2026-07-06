# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

1. Add and manage pets with their basic information.
2. Create and manage pet care tasks such as feeding, walking, medication, and grooming.
3. Generate and view a daily schedule based on task priorities and available time.

### Building Blocks

Owner
- Attributes: name, available_time, preferences, pets
- Methods: add_pet(), get_all_tasks()

Pet
- Attributes: name, species, age, tasks
- Methods: add_task(), remove_task(), get_tasks()

Task
- Attributes: description, duration, priority, task_type, completed
- Methods: mark_complete()

Scheduler
- Attributes: owner
- Methods: generate_daily_plan(), sort_tasks(), filter_tasks()

**a. Initial design**

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler. I designed the system so that each class has a clear responsibility. The Owner class represents the person using the app and stores information about their pets, available time, and preferences. The Pet class stores basic information about each pet and the tasks assigned to it. The Task class represents individual pet care activities, such as feeding, walking, medication, or grooming, along with details like duration, priority, and completion status. Finally, the Scheduler class is responsible for organizing tasks and generating a daily care plan based on priorities and the owner's constraints.



**b. Design changes**

Yes, I made a few small changes after reviewing my UML with the AI coding assistant. I changed the Task priority attribute from a string to an integer because it will make sorting tasks by priority easier later in the project. I also kept Task and Pet as dataclasses while leaving Owner and Scheduler as regular classes, since they are more focused on managing relationships and behavior than simply storing data. Finally, I used `field(default_factory=list)` for list attributes to avoid issues with mutable default values.

**b. Design changes**

Yes, I made several changes after reviewing my UML with the AI coding assistant and implementing the project. I changed the `Task` priority attribute from a string to an integer because it makes sorting tasks by priority easier. I also kept `Task` and `Pet` as dataclasses while leaving `Owner` and `Scheduler` as regular classes since they focus more on behavior than data storage.

As the project evolved, I expanded the design by adding scheduling features such as task time, recurrence, and due dates. I also added new methods like `sort_by_time()`, `filter_by()`, `detect_conflicts()`, `next_occurrence()`, and `complete_task()` to support smarter scheduling, recurring tasks, and conflict detection. These changes made the final system more capable while keeping each class responsible for a specific part of the application.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers several constraints when creating a daily plan, including task priority, the owner's available time, task completion status, scheduled time, and recurring tasks. It also checks for overlapping task times to warn the user about possible scheduling conflicts.

I decided that priority and available time were the most important constraints because they help ensure that the most important pet care tasks are completed first while keeping the schedule realistic for the owner's available time.

**b. Tradeoffs**

My scheduler detects conflicts by comparing every pair of tasks to see if their scheduled times overlap. This approach is simple and easy to understand, but it becomes less efficient as the number of tasks increases because every task must be compared with every other task.

Why this is reasonable? PawPal+ is designed for pet owners who typically manage only a small number of daily tasks. For this type of application, readability and maintainability are more important than optimizing for very large schedules, so the simpler algorithm is a good tradeoff.

I decided to accept the AI suggestion to use itertools.combinations(entries, 2). Even though this is a more Pythonic approach, I found it easier to read than the original nested index loop because it clearly communicates that the algorithm is comparing every pair of tasks. I rejected more advanced optimization ideas because they would make the code harder to understand for this project.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project to brainstorm the initial system design, generate the UML diagram, implement object-oriented classes, improve scheduling algorithms, write docstrings, and create automated tests. I also used AI to review my code and suggest improvements for readability.

The most helpful prompts were specific questions about one method at a time, such as asking how to simplify my conflict detection algorithm or how to write pytest tests for sorting, recurring tasks, and conflict detection.

**b. Judgment and verification**

One suggestion I did not immediately accept was an AI recommendation to optimize the conflict detection algorithm. Instead of making the algorithm more complex, I chose a simpler approach using `itertools.combinations()` because it improved readability without changing the behavior.

I verified every important change by running both the Streamlit application and the automated test suite with `python -m pytest`. I only accepted AI suggestions after confirming they worked correctly.

---

## 4. Testing and Verification

**a. What you tested**

I tested task creation, task completion, adding and removing tasks from pets, sorting by priority and scheduled time, filtering by pet and completion status, recurring daily and weekly tasks, conflict detection, and daily schedule generation.

These tests were important because they verified that the core scheduling logic behaved correctly and that the algorithms continued to work after making changes.

**b. Confidence**

I am very confident that my scheduler works correctly because all 21 automated tests passed successfully. The tests cover the main scheduling features and several edge cases.

If I had more time, I would add tests for more complex recurring schedules, multiple overlapping conflicts, editing existing tasks, and additional invalid user inputs.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the scheduling system became more intelligent throughout the project. Starting from simple classes, I successfully implemented sorting, filtering, recurring tasks, conflict detection, automated tests, and a Streamlit interface that demonstrates these features.

**b. What you would improve**

If I had another iteration, I would improve the Streamlit interface by allowing users to edit or delete existing tasks, mark tasks as completed directly from the UI, and automatically refresh recurring tasks after completion. I would also improve the visual presentation of the schedule.

**c. Key takeaway**

The most important lesson I learned is that AI is a powerful engineering partner, but not a replacement for my own judgment. The best results came from asking focused questions, reviewing every suggestion, testing the code, and deciding which solutions best matched my design goals. Throughout this project, I learned that my role is to be the lead architect, using AI as a tool to improve my work while remaining responsible for the final design and implementation.