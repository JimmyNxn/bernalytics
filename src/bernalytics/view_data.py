"""
View stored job count data from Supabase.

This script retrieves and displays job count data from the Supabase database.
"""

import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from bernalytics.database import DatabaseClient


def format_date(date_str: str) -> str:
    """Format ISO date string to readable format."""
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date.strftime("%Y-%m-%d")
    except:
        return date_str


def display_data(records: list, location: str) -> None:
    """Display job count records in a formatted table."""
    if not records:
        print(f"\nNo data found for location: {location}\n")
        return

    print()
    print("=" * 100)
    print(f"Job Count History for {location}")
    print("=" * 100)
    print(
        f"{'Week Starting':<15} {'Data Engineer':>15} {'Junior':>10} {'Senior':>10} {'Total':>10} {'Collected At':<20}"
    )
    print("-" * 100)

    for record in records:
        week = format_date(record.get("week_starting", ""))
        de = record.get("data_engineer", 0)
        jr = record.get("junior_data_engineer", 0)
        sr = record.get("senior_data_engineer", 0)
        total = de + jr + sr
        collected = format_date(record.get("collected_at", ""))

        print(f"{week:<15} {de:>15} {jr:>10} {sr:>10} {total:>10} {collected:<20}")

    print("=" * 100)
    print(f"Total records: {len(records)}")
    print()


def main(location: str = "Berlin, Germany", limit: int = 10) -> None:
    """
    View job count data from Supabase.

    Args:
        location: Location to query (default: "Berlin, Germany")
        limit: Maximum number of records to retrieve (default: 10)
    """
    # Load environment variables
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        logger.error("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        print("\n❌ Error: Missing Supabase credentials")
        print("Please set SUPABASE_URL and SUPABASE_KEY in your .env file\n")
        return

    try:
        # Initialize database client
        logger.remove()  # Remove default logger
        logger.add(lambda msg: None)  # Suppress logs for cleaner output

        db_client = DatabaseClient(url=supabase_url, key=supabase_key)

        # Fetch data
        records = db_client.get_latest_counts(location=location, limit=limit)

        # Display data
        display_data(records, location)

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="View job count data from Supabase database")
    parser.add_argument(
        "--location",
        type=str,
        default="Berlin, Germany",
        help="Location to query (default: Berlin, Germany)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of records to retrieve (default: 10)",
    )

    args = parser.parse_args()
    main(location=args.location, limit=args.limit)
