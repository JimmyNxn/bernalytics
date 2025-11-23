"""
Database operations for storing job counts in Supabase.

This module provides functions for saving job count data to a PostgreSQL
database via Supabase.
"""

from datetime import datetime
from typing import Optional

from loguru import logger
from supabase import Client, create_client

from bernalytics.models import JobCounts


class DatabaseClient:
    """Client for interacting with Supabase database."""

    def __init__(self, url: str, key: str) -> None:
        """
        Initialize the Supabase client.

        Args:
            url: Supabase project URL
            key: Supabase API key (anon/public key)
        """
        self.client: Client = create_client(url, key)
        logger.info("Supabase client initialized")

    def save_job_counts(
        self,
        counts: JobCounts,
        week_starting: datetime,
        location: str,
    ) -> dict:
        """
        Save job counts to the database.

        Args:
            counts: JobCounts object containing the data
            week_starting: Start date of the week
            location: Location string (e.g., "Berlin, Germany")

        Returns:
            dict: Response from Supabase insert operation

        Raises:
            Exception: If database operation fails
        """
        data = {
            "week_starting": week_starting.date().isoformat(),
            "location": location,
            "data_engineer": counts.data_engineer,
            "junior_data_engineer": counts.junior_data_engineer,
            "senior_data_engineer": counts.senior_data_engineer,
            "collected_at": datetime.utcnow().isoformat(),
        }

        try:
            response = (
                self.client.table("job_counts")
                .upsert(data, on_conflict="week_starting,location")
                .execute()
            )

            logger.success(f"Saved job counts for week {week_starting.date()} in {location}")
            return response.data

        except Exception as e:
            logger.error(f"Failed to save job counts to database: {e}")
            raise

    def get_latest_counts(self, location: str, limit: int = 10) -> list:
        """
        Retrieve the most recent job counts for a location.

        Args:
            location: Location to query
            limit: Maximum number of records to return

        Returns:
            list: List of job count records
        """
        try:
            response = (
                self.client.table("job_counts")
                .select("*")
                .eq("location", location)
                .order("week_starting", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Failed to retrieve job counts: {e}")
            raise
