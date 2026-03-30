from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# Create owner with 90 minutes available today
owner = Owner(name="Alex", availability=90)

# Create two pets
buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

# Add tasks to Buddy
buddy.add_task(Task(description="Morning walk", duration=30, frequency="daily", priority=1))
buddy.add_task(Task(description="Feed breakfast", duration=10, frequency="daily", priority=1))

# Add tasks to Whiskers
whiskers.add_task(Task(description="Give medication", duration=5, frequency="daily", priority=1))
whiskers.add_task(Task(description="Brush fur", duration=15, frequency="weekly", priority=2))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Run the scheduler
scheduler = Scheduler(owner=owner, plan_date=date.today())
scheduler.generate_plan()

print(scheduler.display_plan())
print()
print(scheduler.explain_plan())
