import main


def test_approve_leave_when_no_requests(monkeypatch, capsys):

    monkeypatch.setattr(main, "load_leaves", lambda: [])

    main.approve_leave()

    output = capsys.readouterr().out

    assert "No manager approvals pending." in output

def test_approve_pending_leave(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 7,
            "status": "Manager Approval Required"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr(main, "save_leaves", lambda data: None)
    monkeypatch.setattr("builtins.input", lambda _: "1")

    main.approve_leave()

    assert leaves[0]["status"] == "Approved"

def test_reject_leave_when_no_pending_requests(monkeypatch, capsys):

    monkeypatch.setattr(main, "load_leaves", lambda: [])

    main.reject_leave()

    output = capsys.readouterr().out

    assert "No pending leave requests to reject." in output

def test_reject_pending_leave(monkeypatch):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 7,
            "status": "Manager Approval Required"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr(main, "save_leaves", lambda data: None)
    monkeypatch.setattr("builtins.input", lambda _: "1")

    main.reject_leave()

    assert leaves[0]["status"] == "Rejected"

def test_reject_does_not_change_already_approved_leave(monkeypatch):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 3,
            "status": "Approved"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr(main, "save_leaves", lambda data: None)

    main.reject_leave()

    assert leaves[0]["status"] == "Approved"


def test_approve_leave_rejects_non_numeric_input(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 7,
            "status": "Manager Approval Required"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr("builtins.input", lambda _: "abc")

    main.approve_leave()

    output = capsys.readouterr().out

    assert "Invalid input." in output

def test_approve_leave_rejects_invalid_request_number(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 7,
            "status": "Manager Approval Required"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr("builtins.input", lambda _: "5")

    main.approve_leave()

    output = capsys.readouterr().out

    assert "Invalid request number." in output

def test_reject_leave_rejects_non_numeric_input(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_days": 7,
            "status": "Pending"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)
    monkeypatch.setattr("builtins.input", lambda _: "abc")

    main.reject_leave()

    output = capsys.readouterr().out

    assert "Invalid input." in output