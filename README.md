# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

(.venv) PS C:\Users\hanny\OneDrive\Documentos\Foundations of AI Engineering\ai110-module2show-pawpal-starter> python main.py

Today's PawPal+ Schedule
============================================
  1. Morning walk          30 min  [High  ] walk
  2. Feeding               10 min  [High  ] feeding
  3. Medication            15 min  [Medium] medication
--------------------------------------------
  Total: 55 of 60 min used (5 min free)
============================================

## 🧪 Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The test suite verifies:

- Task creation and completion
- Adding and removing tasks from pets
- Sorting tasks by priority and scheduled time
- Filtering tasks by pet name and completion status
- Automatic creation of recurring daily and weekly tasks
- Conflict detection for overlapping task schedules
- Daily schedule generation
- Edge cases such as invalid time formats and exact time limits

Sample test output:

(.venv) PS C:\Users\hanny\OneDrive\Documentos\Foundations of AI Engineering\ai110-module2show-pawpal-starter> python -m pytest
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\hanny\OneDrive\Documentos\Foundations of AI Engineering\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 21 items                                                                                                                         

tests\test_pawpal.py .....................                                                                                           [100%]

=========================================================== 21 passed in 0.14s ============================================================

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5)

All automated tests passed successfully. The test suite verifies the main scheduling features, including sorting, filtering, recurring tasks, and conflict detection, giving me high confidence that the system works correctly for the expected use cases.


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature          | Method(s)                                                         | Notes                                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_time()` and `Scheduler.sort_tasks()`                 | `sort_by_time()` sorts tasks chronologically by their scheduled time. `sort_tasks()` sorts by priority for the daily plan.                                             |
| Filtering         | `Scheduler.filter_by()` and `Scheduler.filter_tasks()`                  | `filter_by()` filters tasks by pet name and/or completion status. `filter_tasks()` removes completed tasks and keeps tasks that fit within the owner's available time. |
| Conflict handling | `Scheduler.detect_conflicts()`                                          | Detects overlapping task times on the same due date and returns warning messages instead of stopping the program.                                                      |
| Recurring tasks   | `Task.mark_complete()`, `Task.next_occurrence()`, `Pet.complete_task()` | Automatically creates the next daily or weekly task using `timedelta` when a recurring task is completed.                                                              |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
