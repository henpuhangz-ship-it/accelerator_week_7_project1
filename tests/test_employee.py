import main

def test_load_leaves_returns_empty_when_file_missing(tmp_path, monkeypatch):
    test_file = tmp_path/"employees.json"
    monkeypatch.setattr(main,"DATA_FILE",str(test_file))
    assert main.load_leaves()==[]                    

def test_load_leaves_returns_existing_records(tmp_path, monkeypatch):
    test_file = tmp_path/"employees.json"

    test_data = [
        {
            "employee_id":"E001",
            "employee_name": "John",
            "leave-days": 3,
            "status": "Approved"
        }
    ]

    test_file.write_text(__import__("json").dumps(test_data))
    monkeypatch.setattr(main,"DATA_FILE", str(test_file))
    assert main.load_leaves() == test_data

def test_save_leaves_save_records(tmp_path, monkeypatch):
    test_file = tmp_path/"employees.json"
    monkeypatch.setattr(main,"DATA_FILE",str(test_file))
    test_data=[{
                    "employee_id":"E002",
                    "employee_name": "Alice",
                    "leave-days": 2,
                    "status": "Approved"

    }]
    
    main.save_leaves(test_data)
    assert main.load_leaves()==test_data   

def test_view_leaves_displays_records(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "employee_name": "John",
            "leave_type": "Casual Leave",
            "leave_days": 3,
            "reason": "Personal",
            "status": "Approved"
        }
    ]

    monkeypatch.setattr(main, "load_leaves", lambda: leaves)

    main.view_leaves()

    output = capsys.readouterr().out

    assert "John" in output
    assert "E001" in output
    assert "Approved" in output

def test_view_leaves_when_no_records(monkeypatch, capsys):

    monkeypatch.setattr(main, "load_leaves", lambda: [])

    main.view_leaves()

    output = capsys.readouterr().out

    assert "No leave applications found." in output

def test_view_leave_balance(monkeypatch, capsys):

    leaves = [
        {
            "employee_id": "E001",
            "leave_days": 5,
            "status": "Approved"
        },
        {
            "employee_id": "E001",
            "leave_days": 3,
            "status": "Leave Can Be Processed"
        },
        {
            "employee_id": "E001",
            "leave_days": 7,
            "status": "Manager Approval Required"
        },
        {
            "employee_id": "E002",
            "leave_days": 4,
            "status": "Approved"
        }
    ]

    monkeypatch.setattr("builtins.input", lambda _: "E001")
    monkeypatch.setattr(main, "load_leaves", lambda: leaves)

    main.view_leave_balance()

    output = capsys.readouterr().out

    assert "Total Leave: 30" in output
    assert "Used Leave: 8" in output
    assert "Remaining Leave: 22" in output