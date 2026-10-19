
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

    print("\nLeave Types:")
    print("1. Casual Leave")
    print("2. Sick Leave")
    print("3. Earned Leave")

    leave_type_choice = input("Select leave type: ")

    leave_types = {
        "1": "Casual Leave",
        "2": "Sick Leave",
        "3": "Earned Leave"
    }

    if leave_type_choice not in leave_types:
        print("Invalid leave type.")
        return

    leave_type = leave_types[leave_type_choice]

    try:
        leave_days = int(input("Enter number of leave days: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if leave_days <= 0:
        print("Leave days must be greater than zero.")
        return

    reason = input("Enter reason for leave: ")

    if leave_days > 5:
        status = "Manager Approval Required"
    else:
        status = "Leave Can Be Processed"

    leaves = load_leaves()

    leave_request = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "leave_type": leave_type,
        "leave_days": leave_days,
        "reason": reason,
        "status": status
    }

    leaves.append(leave_request)
    save_leaves(leaves)

    print("\nLeave application submitted successfully!")
    print("Status:", status)



def approve_leave():
    leaves = load_leaves()

    pending_requests = [
        (i, leave)
        for i, leave in enumerate(leaves)
        if leave["status"] == "Awaiting Manager Approval"
    ]

    if not pending_requests:
        print("\nNo manager approvals pending.")
        return

    print("\n--- Manager Approval Requests ---")

    for i, leave in pending_requests:
        print(
            f"{i + 1}. {leave['employee_name']} - "
            f"{leave['leave_days']} days"
        )

    try:
        choice = int(input("\nEnter request number to approve: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if choice not in [i for i, leave in pending_requests]:
        print("Invalid request number.")
        return

    leaves[choice]["status"] = "Approved"
    save_leaves(leaves)

    print("\nLeave request approved successfully!")


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
        print("Leave Type:", leave.get("leave_type", "Not specified"))
        print("Leave Days:", leave["leave_days"])
        print("Reason:", leave.get("reason", "Not specified"))
        print("Status:", leave["status"])


def reject_leave():
    leaves = load_leaves()

    pending_requests = [
        (i, leave)
        for i, leave in enumerate(leaves)
        if leave["status"] in ["Pending", "Awaiting Manager Approval"]
    ]

    if not pending_requests:
        print("\nNo pending leave requests to reject.")
        return

    print("\n--- Reject Leave Requests ---")

    for i, leave in pending_requests:
        print(
            f"{i + 1}. {leave['employee_name']} - "
            f"{leave['leave_days']} days - {leave['status']}"
        )

    try:
        choice = int(input("\nEnter request number to reject: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if choice not in [i for i, leave in pending_requests]:
        print("Invalid request number.")
        return

    leaves[choice]["status"] = "Rejected"
    save_leaves(leaves)

    print("\nLeave request rejected successfully!")


def view_leave_balance():
    employee_id = input("Enter Employee ID: ")

    leaves = load_leaves()

    total_leave = 20

    used_leave = sum(
        leave["leave_days"]
        for leave in leaves
        if leave["employee_id"] == employee_id
        and leave["status"] in ["Approved", "Leave Can Be Processed"]
    )

    remaining_leave = total_leave - used_leave

    print("\n--- Employee Leave Balance ---")
    print("Employee ID:", employee_id)
    print("Total Leave:", total_leave)
    print("Used Leave:", used_leave)
    print("Remaining Leave:", remaining_leave)



def main():
    while True:
        print("\n===== Employee Leave Management System =====")
        print("1. Apply for Leave")
        print("2. View Leave Applications")
        print("3. Manager Approval")
        print("4. Reject Leave Request")
        print("5. View Leave Balance")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            apply_leave()

        elif choice == "2":
            view_leaves()

        elif choice == "3":
            approve_leave()

        elif choice == "4":
            reject_leave()

        elif choice == "5":
            view_leave_balance()

        elif choice == "6":
            print("Exiting application...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
