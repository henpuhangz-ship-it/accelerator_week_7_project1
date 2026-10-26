import main
import pytest

@pytest.mark.parametrize(
    "days, expected_status",
    [
        (1, "Leave Can Be Processed"),
        (5, "Leave Can Be Processed"),
        (6, "Manager Approval Required"),
    ]
)

def test_apply_leave(days, expected_status, monkeypatch):
    inputs = iter(["E001", "John", "1", str(days), "Personal"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    saved_data = []

    monkeypatch.setattr(main, "load_leaves", lambda: [])
    monkeypatch.setattr(main, "save_leaves", lambda leaves: saved_data.extend(leaves))

    main.apply_leave()

    assert saved_data[0]["leave_days"]==days
    assert saved_data[0]["status"]==expected_status

def test_apply_leave_rejects_negative_days(monkeypatch, capsys):
    inputs = iter(["E001","John", "1","-3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(main, "load_leaves", lambda: [])
    saved_data = []

    monkeypatch.setattr(main, "save_leaves", lambda leaves: saved_data.extend(leaves))
    main.apply_leave()
    output = capsys.readouterr().out

    assert "Leave days must be greater than zero." in output
    assert saved_data == []

def test_apply_leave_rejects_zero_days(monkeypatch, capsys):

    inputs = iter(["E001", "John", "1", "0"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(main, "load_leaves", lambda: [])

    saved_data = []

    monkeypatch.setattr(
        main,
        "save_leaves",
        lambda leaves: saved_data.extend(leaves)
    )

    main.apply_leave()

    output = capsys.readouterr().out

    assert "Leave days must be greater than zero." in output
    assert saved_data == []

def test_apply_leave_rejects_invalid_leave_type(monkeypatch, capsys):

    inputs = iter(["E001", "John", "9"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.apply_leave()

    output = capsys.readouterr().out

    assert "Invalid leave type." in output

def test_apply_leave_rejects_non_numeric_days(monkeypatch, capsys):

    inputs = iter(["E001", "John", "1", "abc"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.apply_leave()

    output = capsys.readouterr().out

    assert "Please enter a valid number." in output