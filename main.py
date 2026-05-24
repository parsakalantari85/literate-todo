import os
import platform
from manager import TodoList

manager = TodoList()

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def revert_screen():
    input("\nPress Enter to continue... ")

def add_task():
    description = input("Enter task description: ")

    try:
        task_id = manager.add_task(description)

        clear_screen()
        print(f"✓ Added task #{task_id}")

    except ValueError as e:
        clear_screen()
        print(f"✗ Error: {e}")

    revert_screen()

def _print_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            status = "✓ Completed" if task['completed'] else "• Pending"
            created = f"   Created: {task['created_at']}\n" if task['created_at'] else ""

            print(f"{task['id']}. {task['description']}")
            print(f"   Status: {status}")
            print(created, end="")

def list_tasks():
    clear_screen()

    tasks = manager.get_tasks()

    print("╔════════════════════════════════════════════╗")
    print("║                  TODO LIST                 ║")
    print("╚════════════════════════════════════════════╝\n")

    _print_tasks(tasks)

    revert_screen()

def search_tasks():
    query = input("Search tasks: ")

    clear_screen()

    print("╔════════════════════════════════════════════╗")
    print("║                SEARCH RESULTS              ║")
    print("╚════════════════════════════════════════════╝\n")

    results = manager.search_tasks(query)

    if not results:
        print(f'No tasks matching "{query}".')
    else:
        print(f'Found {len(results)} task(s) matching "{query}":\n')
        _print_tasks(results)

    revert_screen()

def complete_task():
    try:
        task_id = int(input("Enter task ID to complete: "))

        manager.mark_completed(task_id)

        clear_screen()
        print(f"✓ Task #{task_id} marked as completed")

    except ValueError as e:
        clear_screen()
        print(f"✗ Error: {e}")

    revert_screen()

def delete_task():
    try:
        task_id = int(input("Enter task ID to delete: "))
        manager.delete_task(task_id)
        clear_screen()
        print(f"✓ Deleted task #{task_id}")

    except ValueError as e:
        clear_screen()
        print(f"✗ Error: {e}")

    revert_screen()

def show_menu():
    clear_screen()

    print("╔════════════════════════════════════════════╗")
    print("║                 TODO LIST                  ║")
    print("╚════════════════════════════════════════════╝\n")

    print("1. Add task")
    print("2. List tasks")
    print("3. Search tasks")
    print("4. Mark task as completed")
    print("5. Delete task")
    print("6. Exit")

def main():
    while True:
        show_menu()

        choice = input("\nChoose (1-6): ")

        if choice == '1':
            add_task()

        elif choice == '2':
            list_tasks()

        elif choice == '3':
            search_tasks()

        elif choice == '4':
            complete_task()

        elif choice == '5':
            delete_task()

        elif choice == '6':
            clear_screen()
            print("Goodbye!")
            break

        else:
            clear_screen()
            print("Invalid choice!")
            revert_screen()

if __name__ == '__main__':
    main()
