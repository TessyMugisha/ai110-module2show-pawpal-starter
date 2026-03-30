import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    task = Task(description="Morning walk", duration=30, frequency="daily")
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed breakfast", duration=10, frequency="daily"))
    assert len(pet.tasks) == 1


def test_owner_filter_tasks_by_pet_and_status():
    owner = Owner(name="Alex", availability=60)
    buddy = Pet(name="Buddy", species="Dog", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", age=5)

    walk = Task(description="Morning walk", duration=30, frequency="daily")
    feed = Task(
        description="Feed breakfast", duration=10, frequency="daily", status="completed"
    )

    buddy.add_task(walk)
    whiskers.add_task(feed)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    assert owner.get_tasks_by_pet("Buddy") == [walk]
    assert owner.get_tasks_by_status("completed") == [feed]
    assert owner.filter_tasks(pet_name="Whiskers") == [feed]
    assert owner.filter_tasks(status="completed") == [feed]
    assert owner.filter_tasks(pet_name="Whiskers", status="completed") == [feed]


def test_daily_task_recurs_next_day():
    yesterday = date.today() - timedelta(days=1)
    task = Task(description="Morning walk", duration=30, frequency="daily")
    task.mark_complete(completion_date=yesterday)

    assert task.is_due(date.today()) is True


def test_mark_complete_creates_next_daily_occurrence():
    owner = Owner(name="Alex", availability=60)
    buddy = Pet(name="Buddy", species="Dog", age=3)
    task = Task(
        description="Morning walk",
        duration=30,
        frequency="daily",
        time="08:00",
    )
    buddy.add_task(task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner=owner, plan_date=date.today())
    next_task = scheduler.mark_task_complete(task)

    assert task.status == "completed"
    assert next_task is not None
    assert next_task is not task
    assert next_task.status == "pending"
    assert next_task.frequency == "daily"
    assert next_task.time == "08:00"
    assert next_task in buddy.tasks
    assert len(buddy.tasks) == 2


def test_scheduler_filters_by_pet():
    owner = Owner(name="Alex", availability=15)
    buddy = Pet(name="Buddy", species="Dog", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", age=5)

    walk = Task(description="Morning walk", duration=10, frequency="daily", priority=1)
    groom = Task(description="Brush fur", duration=10, frequency="daily", priority=2)
    whiskers.add_task(groom)
    buddy.add_task(walk)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    scheduler = Scheduler(owner=owner, plan_date=date.today())
    plan = scheduler.generate_plan(pet_name="Buddy")

    assert plan == [walk]
    assert scheduler.conflicts == []


def test_scheduler_detects_conflicts_for_overfull_day():
    owner = Owner(name="Alex", availability=15)
    buddy = Pet(name="Buddy", species="Dog", age=3)

    walk = Task(description="Morning walk", duration=10, frequency="daily", priority=1)
    groom = Task(description="Brush fur", duration=10, frequency="daily", priority=2)
    buddy.add_task(walk)
    buddy.add_task(groom)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner=owner, plan_date=date.today())
    plan = scheduler.generate_plan()

    assert plan == [walk]
    assert scheduler.conflicts
    assert "could not be scheduled" in scheduler.conflicts[0]


def test_sort_by_time_sorts_tasks_by_hh_mm():
    task_early = Task(
        description="Feed breakfast",
        duration=10,
        frequency="daily",
        time="08:15",
    )
    task_late = Task(
        description="Evening walk",
        duration=20,
        frequency="daily",
        time="18:00",
    )
    task_mid = Task(
        description="Lunch play",
        duration=15,
        frequency="daily",
        time="12:30",
    )

    scheduler = Scheduler(
        owner=Owner(name="Alex", availability=60), plan_date=date.today()
    )
    sorted_tasks = scheduler.sort_by_time([task_mid, task_late, task_early])

    assert sorted_tasks == [task_early, task_mid, task_late]
