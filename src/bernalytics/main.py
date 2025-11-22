"""
Main script for collecting weekly job counts.

Fetches LinkedIn job posting counts and displays results.
"""

from datetime import datetime, timedelta

from loguru import logger

from bernalytics.api.serp_client import SerpClient
from bernalytics.utils.config import get_config


def get_week_start() -> datetime:
    """Get the start of the current week (Monday)."""
    today = datetime.now()
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)


def main() -> None:
    """Collect and display weekly job counts."""
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

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise


if __name__ == "__main__":
    main()
