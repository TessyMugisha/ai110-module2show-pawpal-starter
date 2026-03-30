import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


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
