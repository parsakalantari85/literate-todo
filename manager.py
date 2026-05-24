import csv
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename='tasks.csv'):
        self.filename = filename
        self.initialize_file()

    def initialize_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'description', 'completed', 'created_at'])

    def load_tasks(self):
        tasks = []

        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    tasks.append({
                        'id': int(row['id']),
                        'description': row['description'],
                        'completed': row['completed'] == 'True',
                        'created_at': row.get('created_at', ''),
                    })

        except FileNotFoundError:
            return []

        return tasks

    def save_tasks(self, tasks):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['id', 'description', 'completed', 'created_at'])

            for task in tasks:
                writer.writerow([
                    task['id'],
                    task['description'],
                    task['completed'],
                    task.get('created_at', ''),
                ])

    def add_task(self, description):
        description = description.strip()

        if not description:
            raise ValueError("Task cannot be empty")

        tasks = self.load_tasks()

        new_id = max([task['id'] for task in tasks], default=0) + 1

        tasks.append({
            'id': new_id,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        })

        self.save_tasks(tasks)

        return new_id

    def mark_completed(self, task_id):
        tasks = self.load_tasks()

        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks(tasks)
                return

        raise ValueError(f"Task #{task_id} not found")

    def delete_task(self, task_id):
        tasks = self.load_tasks()

        filtered_tasks = [
            task for task in tasks
            if task['id'] != task_id
        ]

        if len(filtered_tasks) == len(tasks):
            raise ValueError(f"Task #{task_id} not found")

        self.save_tasks(filtered_tasks)

    def get_tasks(self):
        return self.load_tasks()

    def search_tasks(self, query):
        query = query.strip().lower()
        if not query:
            return []
        return [t for t in self.load_tasks() if query in t['description'].lower()]
