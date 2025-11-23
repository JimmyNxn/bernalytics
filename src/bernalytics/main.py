"""
Main script for collecting weekly job counts.

Fetches LinkedIn job posting counts and displays results.
"""

import argparse
import os
from datetime import datetime, timedelta
from typing import Optional

from loguru import logger

from bernalytics.api.serp_client import SerpClient
from bernalytics.database import DatabaseClient
from bernalytics.utils.config import get_config


def get_week_start() -> datetime:
    """Get the start of the current week (Monday)."""
    today = datetime.now()
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)


def main(write_to_db: bool = False) -> None:
    """
    Collect and display weekly job counts.

    Args:
        write_to_db: If True, save results to Supabase database
    """
    # Load configuration
    config = get_config()

    # Setup simple logging
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level="INFO", format="{message}")

    try:
        # Initialize SERP client
        client = SerpClient(api_key=config.serp_api_key)

        # Get job counts
        counts = client.get_job_counts(
            job_title=config.job_title,
            location=config.location,
            time_period=config.time_period,
        )

        week_start = get_week_start()

        # Display results
        print()
        print("=" * 60)
        print(f"Week Starting: {week_start.strftime('%Y-%m-%d')}")
        print(f"Location: {config.location}")
        print("-" * 60)
        print(f'"Data Engineer":          {counts.data_engineer:>4} results')
        print(f'"Junior Data Engineer":   {counts.junior_data_engineer:>4} results')
        print(f'"Senior Data Engineer":   {counts.senior_data_engineer:>4} results')
        print("=" * 60)
        print()

        # Save to database if requested
        if write_to_db:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")

            if not supabase_url or not supabase_key:
                logger.error("SUPABASE_URL and SUPABASE_KEY must be set to write to database")
                raise ValueError("Missing Supabase credentials")

            db_client = DatabaseClient(url=supabase_url, key=supabase_key)
            db_client.save_job_counts(
                counts=counts,
                week_starting=week_start,
                location=config.location,
            )
            print("✅ Data saved to Supabase database\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collect LinkedIn job posting counts for Data Engineering roles"
    )
    parser.add_argument(
        "--write-to-db",
        action="store_true",
        help="Save results to Supabase database",
    )

    args = parser.parse_args()
    main(write_to_db=args.write_to_db)
