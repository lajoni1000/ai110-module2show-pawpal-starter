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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My scheduler detects conflicts by comparing every pair of tasks to see if their scheduled times overlap. This approach is simple and easy to understand, but it becomes less efficient as the number of tasks increases because every task must be compared with every other task.

Why this is reasonable? PawPal+ is designed for pet owners who typically manage only a small number of daily tasks. For this type of application, readability and maintainability are more important than optimizing for very large schedules, so the simpler algorithm is a good tradeoff.

I decided to accept the AI suggestion to use itertools.combinations(entries, 2). Even though this is a more Pythonic approach, I found it easier to read than the original nested index loop because it clearly communicates that the algorithm is comparing every pair of tasks. I rejected more advanced optimization ideas because they would make the code harder to understand for this project.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
