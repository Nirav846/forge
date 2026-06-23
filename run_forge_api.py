#!/usr/bin/env python3
"""FORGE API Server launcher — python run_forge_api.py"""
from src.forge.api_server import run_server

if __name__ == "__main__":
    run_server(host="127.0.0.1", port=8000, reload=False)
