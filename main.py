from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# Create owner with 90 minutes available today
owner = Owner(name="Alex", availability=90)

# Create two pets
buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

# Add tasks out of time order to Buddy
buddy.add_task(
    Task(
        description="Feed dinner",
        duration=10,
        frequency="daily",
        priority=1,
        time="18:00",
    )
)
buddy.add_task(
    Task(
        description="Morning walk",
        duration=30,
        frequency="daily",
        priority=1,
        time="08:00",
    )
)
buddy.add_task(
    Task(
        description="Morning meds",
        duration=5,
        frequency="daily",
        priority=1,
        time="09:00",  # same time as Whiskers' medication — triggers conflict
    )
)
buddy.add_task(
    Task(
        description="Evening play",
        duration=20,
        frequency="daily",
        priority=2,
        time="20:00",
    )
)

# Add tasks out of time order to Whiskers
whiskers.add_task(
    Task(
        description="Brush fur",
        duration=15,
        frequency="weekly",
        priority=2,
        time="12:30",
    )
)
whiskers.add_task(
    Task(
        description="Give medication",
        duration=5,
        frequency="daily",
        priority=1,
        time="09:00",
        status="completed",
    )
)
whiskers.add_task(
    Task(
        description="Feed lunch",
        duration=10,
        frequency="daily",
        priority=1,
        time="13:00",
    )
)

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Print task lists and filters
print("All tasks for Buddy:")
for task in owner.get_tasks_by_pet("Buddy"):
    print(f"- {task.description} at {task.time} [{task.status}]")

print("\nPending tasks for Whiskers:")
for task in owner.filter_tasks(pet_name="Whiskers", status="pending"):
    print(f"- {task.description} at {task.time} [{task.status}]")

print("\nAll completed tasks:")
for task in owner.filter_tasks(status="completed"):
    print(f"- {task.description} ({task.duration} min) for {task.frequency}")

# Run the scheduler and print the plan
scheduler = Scheduler(owner=owner, plan_date=date.today())
scheduler.generate_plan()

print("\nGenerated schedule:")
print(scheduler.display_plan())
print()
print(scheduler.explain_plan())
