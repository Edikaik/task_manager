import json
from typing import List, Optional


class Task:
    """
    Класс Task представляет задачу.
    """
    def __init__(self, task_id: int, title: str, description: str, category: str, due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = task_id  # Уникальный идентификатор задачи
        self.title = title  # Название задачи
        self.description = description  # Описание задачи
        self.category = category  # Категория задачи
        self.due_date = due_date  # Срок выполнения задачи
        self.priority = priority  # Приоритет задачи ("Низкий", "Средний", "Высокий")
        self.status = status  # Статус задачи ("Не выполнена", "Выполнена")

    def to_dict(self):
        """
        Преобразование объекта Task в словарь.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """
        Создание объекта Task из словаря.
        """
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )


class TaskManager:
    """
    Класс TaskManager отвечает за управление задачами.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path  # Путь к файлу для хранения задач
        self.tasks: List[Task] = self.load_tasks()  # Список задач

    def load_tasks(self) -> List[Task]:
        """
        Загрузка задач из файла.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Если файл не найден или поврежден, возвращается пустой список

    def save_tasks(self):
        """
        Сохранение задач в файл.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, task: Task):
        """
        Добавление новой задачи.
        """
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, task_id: int, **updates):
        """
        Редактирование существующей задачи.
        """
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in updates.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.save_tasks()

    def delete_task(self, task_id: int):
        """
        Удаление задачи по ID.
        """
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def mark_completed(self, task_id: int):
        """
        Отметка задачи как выполненной.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.status = "Выполнена"
            self.save_tasks()

    def list_tasks(self, category: Optional[str] = None):
        """
        Просмотр списка задач (всех или по категории).
        """
        return [task for task in self.tasks if not category or task.category == category]

    def search_tasks(self, keyword: str = "", category: Optional[str] = None, status: Optional[str] = None):
        """
        Поиск задач по ключевым словам, категории и статусу.
        """
        return [
            task for task in self.tasks
            if (not category or task.category == category) and
               (not status or task.status == status) and
               (not keyword or keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower())
    ]


    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Получение задачи по ID.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_next_id(self) -> int:
        """
        Получение следующего доступного ID для новой задачи.
        """
        return max((task.id for task in self.tasks), default=0) + 1


def main():
    """
    Главная функция, реализующая консольный интерфейс.
    """
    manager = TaskManager("tasks.json")  # Создаем TaskManager с хранилищем в файле `tasks.json`

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Отметить задачу выполненной")
        print("6. Поиск задач")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            # Просмотр задач
            category = input("Введите категорию (или оставьте пустым): ")
            tasks = manager.list_tasks(category)
            for task in tasks:
                print(f"[{task.id}] {task.title} | {task.category} | {task.due_date} | {task.priority} | {task.status}")
        elif choice == "2":
            # Добавление задачи
            title = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (Низкий, Средний, Высокий): ")
            task = Task(manager.get_next_id(), title, description, category, due_date, priority)
            manager.add_task(task)
            print("Задача добавлена!")
        elif choice == "3":
            # Редактирование задачи
            task_id = int(input("Введите ID задачи: "))
            title = input("Новое название (оставьте пустым, если без изменений): ")
            description = input("Новое описание (оставьте пустым, если без изменений): ")
            updates = {k: v for k, v in [("title", title), ("description", description)] if v}
            manager.edit_task(task_id, **updates)
            print("Задача обновлена!")
        elif choice == "4":
            # Удаление задачи
            task_id = int(input("Введите ID задачи: "))
            manager.delete_task(task_id)
            print("Задача удалена!")
        elif choice == "5":
            # Отметка задачи выполненной
            task_id = int(input("Введите ID задачи: "))
            manager.mark_completed(task_id)
            print("Задача отмечена как выполненная!")
        elif choice == "6":
            # Поиск задач
            keyword = input("Введите ключевое слово: ")
            category = input("Категория (или оставьте пустым): ")
            status = input("Статус (Не выполнена/Выполнена, или оставьте пустым): ")
            tasks = manager.search_tasks(keyword, category, status)
            for task in tasks:
                print(f"[{task.id}] {task.title} | {task.category} | {task.due_date} | {task.priority} | {task.status}")
        elif choice == "7":
            # Выход из программы
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
