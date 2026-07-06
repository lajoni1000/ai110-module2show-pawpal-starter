from datetime import time

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Map the friendly UI labels to the integer priorities the backend sorts by
# (lower number = higher priority).
PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
PRIORITY_LABELS = {1: "High", 2: "Medium", 3: "Low"}

# Keep the Owner in session_state so it (and its pets/tasks) survives reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=60)
owner = st.session_state.owner

st.subheader("Owner")
col_o1, col_o2 = st.columns(2)
with col_o1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col_o2:
    owner.available_time = st.number_input(
        "Available time today (minutes)",
        min_value=1,
        max_value=1440,
        value=owner.available_time,
    )

st.subheader("Add a Pet")
col_p1, col_p2 = st.columns(2)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, age=0))
    st.success(f"Added {pet_name} the {species}.")

st.divider()

st.subheader("Add Tasks")
if not owner.pets:
    st.info("No pets yet. Add a pet above before assigning tasks.")
else:
    pet_names = [pet.name for pet in owner.pets]
    selected_name = st.selectbox("Assign task to", pet_names)
    selected_pet = owner.pets[pet_names.index(selected_name)]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        task_type = st.text_input("Type", value="walk")

    col4, col5 = st.columns(2)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        # Start time drives conflict detection: Scheduler.detect_conflicts() flags
        # tasks whose [start, start + duration) windows overlap on the same day.
        start_time = st.time_input("Start time", value=time(9, 0))

    if st.button("Add task"):
        selected_pet.add_task(
            Task(
                description=task_title,
                duration=int(duration),
                priority=PRIORITY_MAP[priority],
                task_type=task_type,
                time=start_time.strftime("%H:%M"),
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet.name}.")

    # Show each pet's current tasks
    for pet in owner.pets:
        tasks = pet.get_tasks()
        if tasks:
            st.write(f"**{pet.name}** ({pet.species}) — {len(tasks)} task(s):")
            st.table(
                [
                    {
                        "Task": t.description,
                        "Type": t.task_type,
                        "Time": t.time,
                        "Duration (min)": t.duration,
                        "Priority": PRIORITY_LABELS.get(t.priority, t.priority),
                        "Done": t.completed,
                    }
                    for t in tasks
                ]
            )

st.divider()

st.subheader("Build Schedule")

# Let the owner choose how the plan is ordered. "Time of day" uses the
# Scheduler.sort_by_time() method so the plan reads like a real daily timeline;
# "Priority" keeps the generate_daily_plan() order (most important first).
order_by = st.radio(
    "Order the plan by",
    ["Priority", "Time of day"],
    horizontal=True,
)

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()

        if order_by == "Time of day":
            plan = scheduler.sort_by_time(plan)

        if not plan:
            st.info("No tasks fit within the available time.")
        else:
            st.write("### Today's Plan")
            st.table(
                [
                    {
                        "#": i,
                        "Task": t.description,
                        "Type": t.task_type,
                        "Time": t.time,
                        "Duration (min)": t.duration,
                        "Priority": PRIORITY_LABELS.get(t.priority, t.priority),
                    }
                    for i, t in enumerate(plan, start=1)
                ]
            )
            total = sum(t.duration for t in plan)
            st.success(
                f"Total: {total} of {owner.available_time} min used "
                f"({owner.available_time - total} min free)"
            )

        # Surface the algorithmic conflict check. A time overlap is a "careful"
        # signal, not a failure — so it's an st.warning, not st.error. When
        # there are none, say so explicitly instead of leaving the owner guessing.
        conflicts = scheduler.detect_conflicts()
        st.write("### Schedule Check")
        if conflicts:
            st.warning(
                f"Found {len(conflicts)} scheduling conflict(s). "
                "These tasks overlap in time — you may need help or a reschedule:"
            )
            for message in conflicts:
                st.warning(message)
        else:
            st.success("No scheduling conflicts — everything fits without overlaps. 🎉")
