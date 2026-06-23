"""FORGE smoke check — requires the backend to be running.

Usage: python smoke_check_forge.py

Exits with code 0 if all checks pass, 1 on failure.
"""

import sys
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"
PASS, FAIL = 0, 0

def check(label, fn):
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  [PASS] {label}")
    except Exception as e:
        FAIL += 1        # ponytail: first failure stops — caller restarts backend
        print(f"  [FAIL] {label}: {e}")
        print(f"\n  SMOKE CHECK FAILED after {PASS} passed.")
        sys.exit(1)

def api_get(path):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as r:
        return json.loads(r.read())

def api_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def api_delete(path):
    req = urllib.request.Request(f"{BASE}{path}", method="DELETE")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def test_health():
    data = api_get("/api/health")
    assert data.get("status") == "ok", f"Expected status=ok, got {data}"

def test_generate():
    payload = {
        "mode": "core",
        "basics": {"athlete_name": "Smoke Test", "sport": "rugby",
                    "level": "Intermediate", "available_minutes": 60},
        "context": {"primary_goal": "strength"},
        "advanced": {}
    }
    data = api_post("/api/programs/generate", payload)
    assert "weeks" in data, f"Response missing 'weeks': {list(data.keys())}"
    assert len(data["weeks"]) > 0, "Response has empty weeks"

def test_save_artifact():
    global _saved_id
    payload = {"request_payload": {"mode": "core"}, "response_payload": {"program": {"id": "smoke-1"}}}
    data = api_post("/api/programs", payload)
    _saved_id = data.get("id")
    assert _saved_id is not None, f"Save response missing id: {data}"

def test_list_artifacts():
    data = api_get("/api/programs")
    assert isinstance(data, dict) and "artifacts" in data, f"Expected dict with 'artifacts', got {type(data).__name__}"
    assert isinstance(data["artifacts"], list), f"'artifacts' should be a list"
    assert any(a.get("id") == _saved_id for a in data["artifacts"]), f"Saved artifact not in list"

def test_load_artifact():
    data = api_get(f"/api/programs/{_saved_id}")
    assert data.get("id") == _saved_id, f"Loaded wrong artifact: {data}"

def test_delete_artifact():
    data = api_delete(f"/api/programs/{_saved_id}")
    assert "deleted" in data, f"Delete response unexpected: {data}"

def main():
    print(f"\n  FORGE Smoke Check — backend at {BASE}\n")

    checks = [
        ("GET  /api/health", test_health),
        ("POST /api/programs/generate", test_generate),
        ("POST /api/programs  (save artifact)", test_save_artifact),
        ("GET  /api/programs  (list)", test_list_artifacts),
        ("GET  /api/programs/<id>  (load)", test_load_artifact),
        ("DELETE /api/programs/<id>", test_delete_artifact),
    ]

    for label, fn in checks:
        check(label, fn)

    print(f"\n  All {PASS} checks passed. FORGE is working.\n")


if __name__ == "__main__":
    main()
