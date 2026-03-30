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

## Features

- **Pet management** — Add and track multiple pets with name, species, and age. Each pet maintains its own independent task list.
- **Task creation** — Define care tasks with a description, duration (minutes), frequency, priority, and an optional scheduled time (HH:MM).
- **Priority-based scheduling** — The scheduler ranks pending tasks by priority (1 = high) and fits them within the owner's available time for the day.
- **Time-based sorting** — When tasks have an assigned time, the scheduler orders them chronologically so the plan reads like a real daily timeline.
- **Daily recurrence** — Marking a daily or weekly task complete automatically queues a fresh pending copy for the next due date.
- **Conflict warnings** — Surfaces two types of warnings without crashing: tasks that exceed available time, and two tasks assigned to the exact same time slot.
- **Pet and status filtering** — Scope a generated plan to a single pet or filter by completion status.
- **Plan explanation** — After scheduling, the app explains the reasoning (priority order, due date, available time).
- **Streamlit UI** — Interactive interface using `st.table`, `st.success`, and `st.warning` to present the schedule and flag issues clearly.
- **Automated test suite** — 10 pytest tests covering happy paths, edge cases, recurrence, sorting, and conflict detection.

---

## Smarter Scheduling

The `Scheduler` class goes beyond a simple task list:

- **Recurrence awareness** — tasks know their frequency (`daily`, `weekly`, `as needed`) and are only included if they are actually due on the plan date via `is_due()`.
- **Time-based sorting** — if tasks have an optional `HH:MM` time, the scheduler sorts by clock order; otherwise it sorts by priority then shortest duration.
- **Filtering** — `generate_plan()` accepts an optional `pet_name` or `status_filter` to build a plan scoped to one pet or one task state.
- **Conflict detection** — after scheduling, `_find_conflicts()` reports two types of warnings without crashing: tasks that couldn't fit within available time, and tasks assigned to the exact same time slot.
- **Recurring task queue** — marking a daily or weekly task complete automatically clones a new pending instance for the next occurrence.

---

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

- **Task completion** — `mark_complete()` correctly updates task status
- **Task addition** — adding a task to a pet increases its task count
- **Recurrence logic** — a daily task is due again the next day; marking it complete clones a new pending instance
- **Owner filtering** — tasks can be filtered by pet name and/or status
- **Scheduler filtering** — `generate_plan()` can be scoped to a single pet
- **Conflict detection (time)** — warns when two tasks share the exact same time slot
- **Conflict detection (availability)** — warns when due tasks exceed the owner's available time
- **Edge case: empty pet** — a pet with no tasks produces an empty plan with no crashes
- **Sorting correctness** — tasks with `HH:MM` times are returned in chronological order

### Confidence Level
(4/5)

Core scheduling behaviors are well covered. The main gap is duration-overlap detection — two tasks at different times can still overlap in real time, and that is not yet tested.

---

## 📸 Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='C:\PythonProjects\pawPal\ai110-module2show-pawpal-starter\demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

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
