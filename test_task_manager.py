import pytest
from task_manager import Task, TaskManager


@pytest.fixture
def task_manager():
    # Создаем тестовый менеджер задач с временным файлом
    manager = TaskManager("test_tasks.json")
    manager.tasks = []  # Очищаем список задач перед каждым тестом
    return manager


def test_add_task(task_manager):
    task = Task(1, "Тестовая задача", "Описание", "Работа", "2024-12-01", "Высокий")
    task_manager.add_task(task)

    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Тестовая задача"


def test_edit_task(task_manager):
    task = Task(1, "Тестовая задача", "Описание", "Работа", "2024-12-01", "Высокий")
    task_manager.add_task(task)

    task_manager.edit_task(1, title="Обновленное название", description="Новое описание")
    updated_task = task_manager.get_task_by_id(1)

    assert updated_task.title == "Обновленное название"
    assert updated_task.description == "Новое описание"


def test_mark_completed(task_manager):
    task = Task(1, "Тестовая задача", "Описание", "Работа", "2024-12-01", "Высокий")
    task_manager.add_task(task)

    task_manager.mark_completed(1)
    updated_task = task_manager.get_task_by_id(1)

    assert updated_task.status == "Выполнена"


def test_delete_task(task_manager):
    task1 = Task(1, "Задача 1", "Описание 1", "Работа", "2024-12-01", "Высокий")
    task2 = Task(2, "Задача 2", "Описание 2", "Личное", "2024-12-02", "Средний")
    task_manager.add_task(task1)
    task_manager.add_task(task2)

    task_manager.delete_task(1)
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Задача 2"


def test_search_tasks(task_manager):
    task1 = Task(1, "Учеба по Python", "Изучить основы", "Обучение", "2024-12-01", "Высокий")
    task2 = Task(2, "Сходить в магазин", "Купить продукты", "Личное", "2024-12-02", "Средний")
    task_manager.add_task(task1)
    task_manager.add_task(task2)

    results = task_manager.search_tasks(keyword="Python")
    assert len(results) == 1
    assert results[0].title == "Учеба по Python"

    results = task_manager.search_tasks(category="Личное")
    assert len(results) == 1
    assert results[0].title == "Сходить в магазин"

    results = task_manager.search_tasks(status="Не выполнена")
    assert len(results) == 2


def test_list_tasks(task_manager):
    task1 = Task(1, "Задача 1", "Описание 1", "Работа", "2024-12-01", "Высокий")
    task2 = Task(2, "Задача 2", "Описание 2", "Личное", "2024-12-02", "Средний")
    task_manager.add_task(task1)
    task_manager.add_task(task2)

    all_tasks = task_manager.list_tasks()
    assert len(all_tasks) == 2

    work_tasks = task_manager.list_tasks(category="Работа")
    assert len(work_tasks) == 1
    assert work_tasks[0].title == "Задача 1"
