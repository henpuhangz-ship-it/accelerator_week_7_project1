
import json
import os

DATA_FILE = "data/employees.json"


def load_leaves():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_leaves(leaves):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(leaves, file, indent=4)


def apply_leave():
    employee_id = input("Enter Employee ID: ")
    employee_name = input("Enter Employee Name: ")

    try:
        leave_days = int(input("Enter number of leave days: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if leave_days <= 0:
        print("Leave days must be greater than zero.")
        return

    leaves = load_leaves()

    leave_request = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "leave_days": leave_days,
        "status": "Pending"
    }

    leaves.append(leave_request)
    save_leaves(leaves)

    print("\nLeave application submitted successfully!")


def view_leaves():
    leaves = load_leaves()

    if not leaves:
        print("\nNo leave applications found.")
        return

    print("\n--- Employee Leave Records ---")

    for leave in leaves:
        print("----------------------------")
        print("Employee ID:", leave["employee_id"])
        print("Employee Name:", leave["employee_name"])
        print("Leave Days:", leave["leave_days"])
        print("Status:", leave["status"])


def main():
    while True:
        print("\n===== Employee Leave Management System =====")
        print("1. Apply for Leave")
        print("2. View Leave Applications")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            apply_leave()

        elif choice == "2":
            view_leaves()

        elif choice == "3":
            print("Exiting application...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
