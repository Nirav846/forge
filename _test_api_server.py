"""Integration test for the FORGE API server."""
import json
import time
import subprocess
import sys
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8001"

def wait_for_server(timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{BASE}/api/health")
            resp = urllib.request.urlopen(req, timeout=2)
            if resp.status == 200:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def api_post(path, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def api_get(path):
    req = urllib.request.Request(f"{BASE}{path}")
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

def api_delete(path):
    req = urllib.request.Request(f"{BASE}{path}", method="DELETE")
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))

# Start server
server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "src.forge.api_server:app",
     "--host", "127.0.0.1", "--port", "8001"],
    cwd=r"D:\forge",
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
)

passed = 0
failed = 0

try:
    if not wait_for_server():
        print("FAIL: Server did not start")
        sys.exit(1)

    # 1. Health check
    try:
        health = api_get("/api/health")
        assert health["status"] == "ok"
        print(f"PASS: Health check — {health}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Health check — {e}")
        failed += 1

    # 2. Generate program (core mode)
    try:
        payload = {
            "mode": "core",
            "basics": {
                "athlete_name": "Rugby Player",
                "sport": "rugby",
                "level": "Intermediate",
                "frequency_per_week": 3,
                "available_minutes": 60,
            },
            "context": {"primary_goal": "strength"},
            "advanced": {},
        }
        result = api_post("/api/programs/generate", payload)
        assert "summary" in result
        assert "sessions" in result
        assert len(result["sessions"]) > 0
        assert result["summary"]["blueprint_selected"]
        print(f"PASS: Generate (core) — blueprint={result['summary']['blueprint_selected']}, sessions={len(result['sessions'])}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Generate (core) — {e}")
        failed += 1

    # 3. Generate program (premium mode)
    try:
        payload = {
            "mode": "premium",
            "basics": {
                "athlete_name": "Pro Tennis",
                "sport": "tennis",
                "role": "Singles Player",
                "age": 24,
                "level": "Advanced",
                "frequency_per_week": 4,
                "available_minutes": 45,
                "days_to_match": 14,
                "environment": "Commercial Gym",
            },
            "context": {
                "primary_goal": "power",
                "current_phase": "Pre-Season",
            },
            "advanced": {
                "force_velocity_profile": "Velocity Deficit",
                "technique_consistency": "High",
                "injury_risk_flags": ["Right Shoulder"],
            },
        }
        result = api_post("/api/programs/generate", payload)
        assert "summary" in result
        assert result["summary"]["blueprint_selected"]
        print(f"PASS: Generate (premium) — blueprint={result['summary']['blueprint_selected']}, sessions={len(result['sessions'])}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Generate (premium) — {e}")
        failed += 1

    # 4. Generate and then save
    try:
        basic_payload = {
            "mode": "core",
            "basics": {"athlete_name": "Save Test", "sport": "cricket", "level": "Intermediate", "available_minutes": 60},
            "context": {"primary_goal": "conditioning"},
            "advanced": {},
        }
        gen_result = api_post("/api/programs/generate", basic_payload)
        save_result = api_post("/api/programs", {
            "request_payload": basic_payload,
            "response_payload": gen_result,
        })
        assert "id" in save_result
        saved_id = save_result["id"]
        print(f"PASS: Save artifact — id={saved_id}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Save — {e}")
        failed += 1

    # 5. List artifacts
    try:
        listing = api_get("/api/programs")
        assert "artifacts" in listing
        assert len(listing["artifacts"]) >= 1
        print(f"PASS: List artifacts — count={len(listing['artifacts'])}")
        passed += 1
    except Exception as e:
        print(f"FAIL: List — {e}")
        failed += 1

    # 6. Load artifact
    try:
        loaded = api_get(f"/api/programs/{saved_id}")
        assert loaded["id"] == saved_id
        assert "request_snapshot" in loaded
        assert "result_snapshot" in loaded
        print(f"PASS: Load artifact — {loaded['id']}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Load — {e}")
        failed += 1

    # 7. Duplicate artifact
    try:
        dup = api_post(f"/api/programs/{saved_id}/duplicate", {})
        assert dup["id"] != saved_id
        assert dup["duplicated_from"] == saved_id
        print(f"PASS: Duplicate — new_id={dup['id']}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Duplicate — {e}")
        failed += 1

    # 8. Delete artifact
    try:
        delete_result = api_delete(f"/api/programs/{saved_id}")
        assert delete_result["deleted"] == saved_id
        print(f"PASS: Delete artifact — {saved_id}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Delete — {e}")
        failed += 1

    # 9. Generate with minimal payload (missing optional fields)
    try:
        minimal = {
            "mode": "core",
            "basics": {"athlete_name": "Minimal"},
            "context": {},
            "advanced": {},
        }
        result = api_post("/api/programs/generate", minimal)
        assert result["summary"]["blueprint_selected"]
        print(f"PASS: Generate (minimal, no sport) — blueprint={result['summary']['blueprint_selected']}")
        passed += 1
    except Exception as e:
        print(f"FAIL: Generate (minimal) — {e}")
        failed += 1

    # 10. Error handling — invalid endpoint
    try:
        api_get("/api/programs/nonexistent_id_xyz")
        print("FAIL: Load nonexistent should 404")
        failed += 1
    except urllib.error.HTTPError as e:
        assert e.code == 404
        print(f"PASS: Load nonexistent returns 404")
        passed += 1
    except Exception as e:
        print(f"FAIL: Load nonexistent — {e}")
        failed += 1

finally:
    server.terminate()
    server.wait(timeout=5)
    # Cleanup test artifacts
    import os, glob
    for f in glob.glob(r"D:\forge\.forge_artifacts\*.json"):
        os.remove(f)

print(f"\n=== Results: {passed} passed, {failed} failed ===")
sys.exit(0 if failed == 0 else 1)
