# Bernalytics - Just commands

# Show available commands
default:
    @just --list

# Setup: Install dependencies
setup:
    uv venv
    uv pip install -e .

# Run: Collect and display job counts
run:
    uv run python -m bernalytics.main

# Run with database: Collect, display, and save to Supabase
run-db:
    uv run python -m bernalytics.main --write-to-db

# Test: Run all tests
test:
    pytest

# Clean: Remove generated files
clean:
    rm -rf .pytest_cache htmlcov .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
