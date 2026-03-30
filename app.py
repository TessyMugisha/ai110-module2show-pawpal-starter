from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart daily planner for busy pet owners.")

# ── Owner setup ──────────────────────────────────────────────────────────────
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Alex")
with col2:
    availability = st.number_input(
        "Time available today (minutes)", min_value=5, max_value=480, value=90
    )

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, availability=int(availability))
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.availability = int(availability)

# ── Pets ─────────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Pets")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Buddy", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"], key="species_input")
with col3:
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=3, key="pet_age_input")

if st.button("Add pet"):
    existing_names = [p.name for p in st.session_state.owner.pets]
    if pet_name in existing_names:
        st.warning(f"A pet named '{pet_name}' is already added.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species, age=int(pet_age)))
        st.success(f"Added {pet_name} the {species}!")

if st.session_state.owner.pets:
    st.table(
        [{"Name": p.name, "Species": p.species, "Age": p.age}
         for p in st.session_state.owner.pets]
    )
else:
    st.info("No pets yet — add one above to start scheduling tasks.")

# ── Tasks ─────────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Tasks")

if st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        selected_pet_name = st.selectbox("Pet", pet_names, key="task_pet_select")
    with col2:
        task_desc = st.text_input("Description", value="Morning walk", key="task_desc_input")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="duration_input")
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], key="freq_input")
    with col5:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"], key="priority_input")

    task_time = st.text_input(
        "Scheduled time (HH:MM, optional)", value="", placeholder="e.g. 09:00", key="time_input"
    )

    priority_map = {"high": 1, "medium": 2, "low": 3}

    if st.button("Add task"):
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        new_task = Task(
            description=task_desc,
            duration=int(duration),
            frequency=frequency,
            priority=priority_map[priority_label],
            time=task_time.strip() or None,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_desc}' to {selected_pet_name}.")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.table([
            {
                "Pet": t.pet.name if t.pet else "—",
                "Task": t.description,
                "Duration": f"{t.duration} min",
                "Frequency": t.frequency,
                "Priority": t.priority,
                "Time": t.time or "—",
                "Status": t.status,
            }
            for t in all_tasks
        ])
    else:
        st.info("No tasks yet — add one above.")
else:
    st.info("Add a pet first before adding tasks.")

# ── Schedule ──────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Today's Schedule")

filter_pet = st.selectbox(
    "Filter by pet (optional)",
    ["All pets"] + [p.name for p in st.session_state.owner.pets],
    key="filter_pet_select",
)

if st.button("Generate schedule"):
    if not st.session_state.owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner, plan_date=date.today())
        pet_filter = None if filter_pet == "All pets" else filter_pet
        scheduled = scheduler.generate_plan(pet_name=pet_filter)

        if not scheduled:
            st.warning("No due tasks fit within your available time today.")
        else:
            st.success(f"{len(scheduled)} task(s) scheduled for today.")
            st.table([
                {
                    "Pet": t.pet.name if t.pet else "—",
                    "Task": t.description,
                    "Duration": f"{t.duration} min",
                    "Time": t.time or "—",
                    "Priority": t.priority,
                }
                for t in scheduled
            ])

        st.markdown("**Why this plan?**")
        st.info(scheduler.explain_plan())

        if scheduler.conflicts:
            st.markdown("**Warnings**")
            for msg in scheduler.conflicts:
                st.warning(msg)
