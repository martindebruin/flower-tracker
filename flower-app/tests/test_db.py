import pytest
import sqlite3
import db

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, 'DB_PATH', str(tmp_path / 'test.db'))
    db.init_db()

def test_get_latest_empty():
    assert db.get_latest() is None

def test_save_and_get_latest():
    db.save_reading('2026-06-02T14:00:00', 'wet', 'dry')
    r = db.get_latest()
    assert r['ettan'] == 'wet'
    assert r['spansk_timjan'] == 'dry'
    assert r['timestamp'] == '2026-06-02T14:00:00'

def test_latest_is_most_recent():
    db.save_reading('2026-06-02T12:00:00', 'wet', 'wet')
    db.save_reading('2026-06-02T14:00:00', 'dry', 'dry')
    r = db.get_latest()
    assert r['timestamp'] == '2026-06-02T14:00:00'

def test_cleanup_deletes_old_rows():
    db.save_reading('2020-01-01T00:00:00', 'wet', 'wet')
    db.save_reading('2026-06-02T14:00:00', 'dry', 'dry')
    db.save_reading('2026-06-02T15:00:00', 'wet', 'wet')
    with sqlite3.connect(db.DB_PATH) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM readings WHERE timestamp = '2020-01-01T00:00:00'"
        ).fetchone()[0]
    assert count == 0
