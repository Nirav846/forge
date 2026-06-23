"""FORGE local environment validation script.

Safe to run without launching servers.
Prints PASS / WARN / FAIL for each check.
"""

import os
import sys
import importlib.util
import subprocess
import shutil

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def _fmt(status: str, label: str, detail: str = ""):
    icons = {"PASS": "[OK]", "WARN": "[!]", "FAIL": "[X]"}
    icon = icons.get(status, "[?]")
    print(f"  {icon}  {status:5s}  {label}")
    if detail:
        print(f"            {detail}")


def check_python():
    v = sys.version_info
    if v.major >= 3 and v.minor >= 10:
        _fmt("PASS", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        _fmt("FAIL", f"Python {v.major}.{v.minor}.{v.micro} (need 3.10+)", "Upgrade Python")


def check_import(mod_name: str, label: str = ""):
    try:
        importlib.import_module(mod_name)
        _fmt("PASS", f"Package '{mod_name}' importable")
    except ImportError:
        _fmt("FAIL", f"Package '{mod_name}' not found", f"Run: pip install {label or mod_name}")


def check_file(path: str, label: str = ""):
    full = os.path.join(REPO_ROOT, path) if not os.path.isabs(path) else path
    if os.path.exists(full):
        _fmt("PASS", f"File exists: {path}")
    else:
        _fmt("FAIL", f"File missing: {path}", label or "")


def check_dir(path: str, label: str = ""):
    full = os.path.join(REPO_ROOT, path) if not os.path.isabs(path) else path
    if os.path.isdir(full):
        _fmt("PASS", f"Directory exists: {path}")
    else:
        _fmt("FAIL", f"Directory missing: {path}", label)


def check_can_create_artifacts():
    """Test that the artifact storage directory is creatable."""
    test_dir = os.path.join(REPO_ROOT, ".forge_artifacts")
    try:
        os.makedirs(test_dir, exist_ok=True)
        _fmt("PASS", "Artifact storage dir accessible")
    except (OSError, PermissionError) as e:
        _fmt("FAIL", "Cannot create artifact storage dir", str(e))


def check_npm():
    npm = shutil.which("npm")
    if npm:
        try:
            out = subprocess.check_output([npm, "--version"], text=True, stderr=subprocess.STDOUT, timeout=10)
            _fmt("PASS", f"npm {out.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            _fmt("FAIL", "npm not functional", "Install Node.js / npm")
    else:
        _fmt("FAIL", "npm not found on PATH", "Install Node.js / npm")


def check_frontend_modules():
    node_modules = os.path.join(REPO_ROOT, "forge_web", "node_modules")
    if os.path.isdir(node_modules):
        _fmt("PASS", "Frontend node_modules exists")
    else:
        _fmt("WARN", "Frontend node_modules missing", "Run: cd forge_web && npm install")


def check_bat_files():
    for bat in ["start_forge.bat", "stop_forge.bat"]:
        full = os.path.join(REPO_ROOT, bat)
        if os.path.exists(full):
            _fmt("PASS", f"BAT file exists: {bat}")
        else:
            _fmt("WARN", f"BAT file missing: {bat}")


def main():
    print(f"\n{'='*50}")
    print("  FORGE — Local Environment Validation")
    print(f"{'='*50}\n")

    checks = [
        ("Python", check_python),
        ("Backend imports", lambda: [
            check_import("fastapi", "fastapi"),
            check_import("uvicorn", "uvicorn"),
            check_import("pydantic", "pydantic"),
            check_import("src.forge.main", "(FORGE source)"),
            check_import("src.forge.api_server", "(FORGE source)"),
        ]),
        ("Project files", lambda: [
            check_dir("src/forge", "Backend source"),
            check_dir("forge_web", "Frontend source"),
            check_file("forge_web/package.json", "Frontend package manifest"),
            check_file("requirements.txt", "pip install -r requirements.txt"),
        ]),
        ("Artifact storage", check_can_create_artifacts),
        ("Startup scripts", lambda: [
            check_file("run_forge_api.py"),
            check_bat_files(),
        ]),
        ("Node / npm", check_npm),
        ("Frontend deps", check_frontend_modules),
    ]

    all_pass = True
    for section_name, fn in checks:
        print(f"  [{section_name}]")
        fn()
        print()

    print(f"{'='*50}")
    print("  To launch FORGE:")
    print("    start_forge.bat")
    print("  Or manually:")
    print("    Terminal 1: python run_forge_api.py")
    print("    Terminal 2: cd forge_web && npm run dev")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
