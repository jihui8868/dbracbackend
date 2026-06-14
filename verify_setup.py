#!/usr/bin/env python
"""Verification script to check if the FastAPI application is properly set up."""

import sys
import importlib.util
from pathlib import Path


def check_file(file_path: Path, name: str) -> bool:
    if file_path.exists():
        print(f"✓ {name}")
        return True
    else:
        print(f"✗ {name} - NOT FOUND")
        return False


def check_import(module_name: str, name: str) -> bool:
    try:
        __import__(module_name)
        print(f"✓ {name}")
        return True
    except ImportError as e:
        print(f"✗ {name} - {e}")
        return False


def main():
    print("=" * 60)
    print("DBRCA FastAPI Application - Setup Verification")
    print("=" * 60)

    backend_path = Path(__file__).parent
    all_good = True

    # Check essential files
    print("\n📋 Checking essential files...")
    essential_files = [
        (backend_path / "app" / "main.py", "app/main.py"),
        (backend_path / "main.py", "main.py (entry point)"),
        (backend_path / ".env.example", ".env.example"),
        (backend_path / "README.md", "README.md"),
        (backend_path / "pyproject.toml", "pyproject.toml"),
    ]

    for file_path, name in essential_files:
        if not check_file(file_path, name):
            all_good = False

    # Check app structure
    print("\n📁 Checking app directory structure...")
    app_files = [
        (backend_path / "app" / "__init__.py", "app/__init__.py"),
        (backend_path / "app" / "core" / "config.py", "app/core/config.py"),
        (backend_path / "app" / "core" / "database.py", "app/core/database.py"),
        (backend_path / "app" / "models" / "user.py", "app/models/user.py"),
        (backend_path / "app" / "models" / "conversation.py", "app/models/conversation.py"),
        (backend_path / "app" / "schemas" / "user.py", "app/schemas/user.py"),
        (backend_path / "app" / "schemas" / "chat.py", "app/schemas/chat.py"),
        (backend_path / "app" / "crud" / "user.py", "app/crud/user.py"),
        (backend_path / "app" / "crud" / "conversation.py", "app/crud/conversation.py"),
        (backend_path / "app" / "router" / "auth.py", "app/router/auth.py"),
        (backend_path / "app" / "router" / "chat.py", "app/router/chat.py"),
        (backend_path / "app" / "agents" / "main_agent.py", "app/agents/main_agent.py"),
        (backend_path / "app" / "agents" / "subagents" / "tools.py", "app/agents/subagents/tools.py"),
    ]

    for file_path, name in app_files:
        if not check_file(file_path, name):
            all_good = False

    # Check Python imports
    print("\n🐍 Checking Python imports...")
    imports = [
        ("app.core.config", "Config"),
        ("app.core.database", "Database"),
        ("app.models.user", "User model"),
        ("app.models.conversation", "Conversation model"),
        ("app.schemas.user", "User schemas"),
        ("app.schemas.chat", "Chat schemas"),
        ("app.crud.user", "User CRUD"),
        ("app.crud.conversation", "Conversation CRUD"),
        ("app.router.auth", "Auth router"),
        ("app.router.chat", "Chat router"),
        ("app.agents.main_agent", "Agent"),
    ]

    for module_name, name in imports:
        if not check_import(module_name, name):
            all_good = False

    # Check FastAPI app
    print("\n🚀 Checking FastAPI app...")
    try:
        from app.main import app

        print(f"✓ FastAPI app created")
        print(f"  Title: {app.title}")
        print(f"  Routes: {len(app.routes)} total")

        route_names = [
            "/auth/register",
            "/auth/login",
            "/auth/me",
            "/chat/sessions",
            "/chat/{conversation_id}/message",
            "/health",
        ]

        routes_found = {name: False for name in route_names}
        for route in app.routes:
            if hasattr(route, "path"):
                for route_name in route_names:
                    if route_name in route.path:
                        routes_found[route_name] = True

        for route_name, found in routes_found.items():
            status = "✓" if found else "✗"
            print(f"  {status} {route_name}")
            if not found:
                all_good = False

    except Exception as e:
        print(f"✗ FastAPI app - {e}")
        all_good = False

    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All checks passed! Application is ready to run.")
        print("\nTo start the server:")
        print("  uv run uvicorn app.main:app --reload")
        print("\nOr with Python directly:")
        print("  uv run python main.py")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
